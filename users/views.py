import locale
import logging
import json
import os
import uuid
from storages.backends.s3boto3 import S3Boto3Storage
from botocore.exceptions import ClientError
from decimal import Decimal
from django.http import JsonResponse
from django.db import transaction as db_transaction
from django.core.exceptions import ValidationError

from django.contrib import messages

from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db import \
    transaction as db_transaction  # Ensure atomic transactions
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.utils.timezone import now

from .filters import TransactionFilter
from .forms import (DomesticTransferForm, InternationalTransferForm,
                    LocalTransferForm, Profile_pictureForm, ProfileForm,
                    ProfileFormLite)
from .models import (AccountNumber, DomesticTransfer, InternationalTransfer,
                     LocalTransfer, Profile, Transaction)
from .utils import check_account_locked

# Initialize a logger for error tracking
logger = logging.getLogger(__name__)


class MediaStorage(S3Boto3Storage):
    location = "media"
    file_overwrite = False


@login_required
def manage_profile(request):
    # Get the user's profile or create one if it doesn't exist
    profile, created = Profile.objects.get_or_create(user=request.user)

    if request.method == 'POST':
        form = ProfileFormLite(request.POST, instance=profile)
        if form.is_valid():
            # Update user first name and last name
            request.user.first_name = form.cleaned_data['first_name']
            request.user.last_name = form.cleaned_data['last_name']
            request.user.save()  # Save user data

            form.save()  # Save profile data

            # Redirect to a profile view or another page
            return redirect('profile')
    else:
        form = ProfileForm(instance=profile)

    context = {'form': form, 'created': created}

    return render(request, 'profiles/manage_profile.html', context)


@login_required
def manage_profile_image(request):
    # Get the user's profile or create one if it doesn't exist
    profile, created = Profile.objects.get_or_create(user=request.user)
    profile_picture_url = ''
    print("Generating URL from Start", profile_picture_url)

    # Generate a presigned URL for the profile picture if it exists
    if profile.profile_picture:
        try:
            # Use MediaStorage location to correctly generate the S3 key
            s3_key = f"{profile.profile_picture.name}"
            presigned_url = settings.S3_CLIENT.generate_presigned_url(
                'get_object',
                Params={
                    'Bucket': settings.AWS_STORAGE_BUCKET_NAME,
                    'Key': s3_key,
                },
                ExpiresIn=3600,  # URL valid for 1 hour
            )
            # Set the presigned URL to be used in the template
            profile_picture_url = presigned_url
            print("Generating URL from get inside function", presigned_url)
        except ClientError as e:
            messages.error(request, f"Failed to generate URL: {str(e)}")
            presigned_url = ""
    else:
        presigned_url = ""  # No profile picture

    print("Generating URL from get", presigned_url)

    if request.method == 'POST':
        form = Profile_pictureForm(
            request.POST, request.FILES, instance=profile)

        if form.is_valid():
            # Handle file upload
            # Assuming 'profile_picture' is the form field name
            file = request.FILES.get('profile_picture')
            print("File is ", file)
            if not file:
                messages.error(request, 'Please select a file')

            # Validate file type and size
            allowed_types = ['image/jpeg',
                             'image/png', 'image/gif', 'image/webp']
            if file.content_type not in allowed_types:
                messages.error(
                    request, f"Invalid file type. Allowed types: {', '.join(allowed_types)}")
                return redirect('profile')

            max_file_size = 5 * 1024 * 1024  # 5MB
            if file.size > max_file_size:
                messages.error(request, "File size exceeds the 5MB limit.")
                return redirect('profile')

            try:
                # Create a unique file key to avoid collisions
                file_extension = os.path.splitext(
                    file.name)[1].lower()  # Get file extension
                unique_filename = f"test/{uuid.uuid4().hex}{file_extension}"

                # Upload file to AWS S3
                try:
                    settings.S3_CLIENT.upload_fileobj(
                        file,
                        settings.AWS_STORAGE_BUCKET_NAME,
                        f"{MediaStorage.location}/{unique_filename}",
                        ExtraArgs={'ContentType': file.content_type},
                    )
                except ClientError as e:
                    messages.error(request, f"Failed to upload file: {str(e)}")
                    return redirect('profile')

                # Save the S3 file key to the profile
                profile.profile_picture = f"{MediaStorage.location}/{unique_filename}"
                profile.save()

                # Generate the presigned URL for the updated profile picture
                s3_key = f"{MediaStorage.location}/{unique_filename}"
                try:
                    presigned_url = settings.S3_CLIENT.generate_presigned_url(
                        'get_object',
                        Params={
                            'Bucket': settings.AWS_STORAGE_BUCKET_NAME,
                            'Key': s3_key,
                        },
                        ExpiresIn=3600,  # URL valid for 1 hour
                    )
                except ClientError as e:
                    messages.error(
                        request, f"Failed to generate presigned URL: {str(e)}")

                print("Generating URL from post", presigned_url)

                # Success message
                messages.success(
                    request, 'Your profile picture has been updated successfully!')
                return redirect('profile')

            except Exception as e:
                messages.error(
                    request, f"Error uploading the profile picture: {str(e)}")
                return redirect('profile')
        else:
            messages.error(request, 'Invalid form data.')
    else:
        messages.error(request, 'Unable to update your profile picture!')

    # Context includes the presigned URL if available
    context = {'form': form, 'created': created, 'iurl': profile_picture_url}
    return render(request, 'profiles/profile.html', context)

# Delete Profile Picture


@login_required
def delete_profile_image(request):
    # Get or create the user's profile
    profile, created = Profile.objects.get_or_create(user=request.user)

    if request.method == 'POST':
        if profile.profile_picture:
            profile.profile_picture.delete()  # Delete the file from storage
            profile.profile_picture = None     # Clear the field
            profile.save()                     # Save the changes

            messages.success(
                request, 'Your profile picture has been deleted successfully!')
            # log_action(request.user, DELETION, f"Deleted profile_picture for {
            #            request.user.username}", profile)

            return redirect('profile')  # Redirect to the profile view
        else:
            messages.error(request, 'No profile picture to delete.')

    # Redirect in case of a GET request or other methods
    return redirect('profile')


@login_required
def user_profile(request):
    try:
        profile = Profile.objects.get(user=request.user)
    except Profile.DoesNotExist:
        # log_action(request.user, ADDITION, f"Attempted to view/edit profile for {
        #            request.user.username}, but no profile exists.")
        profile = Profile(user=request.user)
        profile.save()

    if request.method == 'POST':
        form = ProfileFormLite(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            # log_action(request.user, CHANGE, f"Updated profile for {
            #            request.user.username}", profile)
            messages.success(request, "Profile updated successfully!")
            return redirect('user_profile')
    else:
        form = ProfileFormLite(instance=profile)
        # messages.error(request, "Profile updated unsuccessfully!")

    profile_picture_url = ''

    # Generate a presigned URL for the profile picture if it exists
    if profile.profile_picture:
        try:
            # Use MediaStorage location to correctly generate the S3 key
            s3_key = f"{profile.profile_picture.name}"
            presigned_url = settings.S3_CLIENT.generate_presigned_url(
                'get_object',
                Params={
                    'Bucket': settings.AWS_STORAGE_BUCKET_NAME,
                    'Key': s3_key,
                },
                ExpiresIn=3600,  # URL valid for 1 hour
            )
            # Set the presigned URL to be used in the template
            profile_picture_url = presigned_url
        except ClientError as e:
            messages.error(request, f"Failed to generate URL: {str(e)}")
            presigned_url = ""
    else:
        presigned_url = ""  # No profile picture

    profile_picture_url = presigned_url

    # profile_picture_url = request.build_absolute_uri(
    #     profile.profile_picture.url) if profile.profile_picture else ""

    if request.method == 'GET':
        pass
        # log_action(request.user, ADDITION, f"Viewed profile for {
        #            request.user.username}", profile)

    context = {
        'profile': profile,
        'form': form,
        'iurl': profile_picture_url
    }

    return render(request, 'profiles/profile.html', context)


@login_required
def domesticTransaction(request):
    try:
        locale.setlocale(locale.LC_ALL, 'en_US.UTF-8')
    except locale.Error:
        locale.setlocale(locale.LC_ALL, '')

    account, created = AccountNumber.objects.get_or_create(user=request.user)

    try:
        account_balance = locale.currency(
            account.account_balance, grouping=True, symbol=False)
    except locale.Error:
        account_balance = f"{account.account_balance:,.2f}"

    company_name = settings.COMPANY_NAME

    if account.locked:
        messages.error(
            request, "Account is locked. Contact support.")
        return redirect('dashboard')

    try:
        account_balance = get_account_balance(request)
        if not account.password:
            messages.error(
                request, 'You need to set a password before proceeding with transactions.')
            # Redirect to a suitable page
            return redirect('set_password')

    except AccountNumber.DoesNotExist:
        messages.error(
            request, "Your account could not be found. Please contact customer support.")
        return redirect('dashboard')

    if request.method == 'POST':
        data = json.loads(request.body)
        bank_name = data.get('bankName')
        amount = data.get('amount')
        password = data.get('password')
        bank_account = data.get('accountNumber')
        beneficiary = data.get('accountName')
        description = data.get('description')

        if not all([amount, beneficiary, password, bank_name, bank_account, description]):
            return JsonResponse({'error': 'Missing required fields.'}, status=400)

        try:
            with db_transaction.atomic():
                amount_decimal = Decimal(amount)

                if account.locked:
                    messages.error(
                        request, "Account is locked. Contact support.")
                    return redirect('dashboard')

                if not account.check_password(password):
                    return JsonResponse({'error': 'Incorrect password'}, status=400)

                domestic_transfer = DomesticTransfer.objects.create(
                    user=request.user,
                    beneficiary=bank_name,
                    bank_account=int(bank_account),
                    description=description,
                    amount=amount_decimal,
                    updated=now(),
                )

                # Deduct the amount from the user's account balance
                domestic_transfer.transfer(amount, password)

                Transaction.objects.create(
                    wallet=account,
                    transaction_type='domestic_transfer',
                    to_user=beneficiary,
                    incoming='Debit',
                    amount=amount_decimal,
                    updated=now()
                )

                messages.success(request, f'''Transaction to {
                                 beneficiary} successful''')
                return JsonResponse({'message': f'Transaction to {beneficiary} successful'}, status=200)

        except ValidationError as e:
            logger.error(f"Validation Error: {e}")
            error_message = e.messages[0] if hasattr(
                e, 'messages') and e.messages else str(e)
            return JsonResponse({'error': error_message}, status=400)

        except Exception as e:
            logger.error(f"Error saving transaction: {e}")
            return JsonResponse({'error': 'An unexpected error occurred. Please try again.'}, status=500)

    return render(request, 'dashboard/domestic-transfer.html', {
        'account_balance': account_balance,
        'account_balance_noformat': account.account_balance,
        "company_name": company_name,
    })


@login_required
def set_password(request):
    if request.method == 'POST':
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')

        if password and password == confirm_password:
            account = AccountNumber.objects.get(user=request.user)
            account.set_password(password)
            messages.success(
                request, "Password set successfully. You can now perform transactions.")
            return redirect('dashboard')
        else:
            messages.error(
                request, "Passwords do not match. Please try again.")

    return render(request, 'dashboard/set_password.html', {'title': 'Set Password'})


@login_required
def localTransaction(request):
    # Set locale for currency formatting
    try:
        locale.setlocale(locale.LC_ALL, 'en_US.UTF-8')
    except locale.Error:
        locale.setlocale(locale.LC_ALL, '')

    # Retrieve or create the user's account
    account, created = AccountNumber.objects.get_or_create(user=request.user)

    # Handle account balance formatting
    try:
        account_balance = locale.currency(
            account.account_balance, grouping=True, symbol=False)
    except locale.Error:
        account_balance = f"{account.account_balance:,.2f}"

    # Check if the account is locked
    if account.locked:
        messages.error(
            request, "Your account is locked. Please contact support.")
        return redirect('dashboard')

    # Ensure the account has a password
    if not account.password:
        messages.error(
            request, "Please set a password before proceeding with transactions.")
        return redirect('set_password')

    # Handle POST request for transaction
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            account_number = data.get('accountNumber')
            amount = data.get('amount')
            password = data.get('password')
            description = data.get('description')

            # Validate required fields
            if not all([account_number, amount, password, description]):
                return JsonResponse({'error': 'All fields are required.'}, status=400)

            # Fetch receiver details
            receiver = get_object_or_404(
                AccountNumber, account_number=int(account_number))

            # Prevent transferring to self
            if receiver.user == request.user:
                return JsonResponse({'error': 'You cannot transfer to your own account.'}, status=400)

            # Perform the transaction
            with db_transaction.atomic():
                # Check account lock again (race condition prevention)
                if account.locked:
                    return JsonResponse({'error': 'Your account is locked. Please contact support.'}, status=403)

                # Verify password
                if not account.check_password(password):
                    return JsonResponse({'error': 'Incorrect password.'}, status=400)

                # Deduct amount and create LocalTransfer instance
                local_transfer = LocalTransfer.objects.create(
                    user=request.user,
                    account=receiver,
                    description=description,
                    amount=Decimal(amount),
                    updated=now()
                )
                local_transfer.transfer(amount, password)

                # Log the transaction
                Transaction.objects.create(
                    wallet=account,
                    transaction_type='local_transfer',
                    to_user=receiver.user,
                    incoming='Debit',
                    amount=Decimal(amount),
                    updated=now()
                )

                messages.success(
                    request, "Transaction processed successfully.")
                return JsonResponse({'message': 'Transaction completed successfully.'}, status=200)

        except AccountNumber.DoesNotExist:
            logger.error("Receiver account not found.")
            return JsonResponse({'error': 'Receiver account not found.'}, status=404)

        except ValidationError as e:
            logger.error(f"Validation Error: {e}")
            return JsonResponse({'error': str(e)}, status=400)

        except Exception as e:
            logger.error(f"Unexpected error during transaction: {e}")
            return JsonResponse({'error': 'An unexpected error occurred. Please try again.'}, status=500)

    return render(request, 'dashboard/local-transfer.html', {
        'account_balance': account_balance,
        'account_balance_noformat': account.account_balance,
        'company_name': settings.COMPANY_NAME,
    })


def get_receiver_details(account_number):
    """Fetch receiver details by account number."""
    return get_object_or_404(AccountNumber, account_number=account_number)


@login_required
def check_receiver(request, account_number):
    """Check if the receiver exists and is valid."""
    try:
        print("Checking")
        print("Account number is ", account_number)
        print("Account number is type", type(int(account_number)))

        # Attempt to retrieve the receiver's account
        receiver = AccountNumber.objects.get(account_number=account_number)

        # Prevent transferring to self
        if receiver.user == request.user:
            return JsonResponse({'error': 'You cannot transfer to your own account.'}, status=400)

        # If everything is valid, return success response
        return JsonResponse({'message': f'{receiver.user.first_name} {receiver.user.last_name}'}, status=200)

    except AccountNumber.DoesNotExist:
        # Handle the case where the account does not exist
        return JsonResponse({'error': 'Receiver account not found.'}, status=404)

    except ValueError:
        # Handle invalid account number format (e.g., non-integer input)
        return JsonResponse({'error': 'Invalid account number format.'}, status=400)


@login_required
def internationalTransaction(request):
    # Set locale for currency formatting
    try:
        locale.setlocale(locale.LC_ALL, 'en_US.UTF-8')
    except locale.Error:
        locale.setlocale(locale.LC_ALL, '')

    # Retrieve or create the user's account
    account, created = AccountNumber.objects.get_or_create(user=request.user)

    # Handle account balance formatting
    try:
        account_balance = locale.currency(
            account.account_balance, grouping=True, symbol=False)
    except locale.Error:
        account_balance = f"{account.account_balance:,.2f}"

    # Check if the account is locked
    if account.locked:
        return JsonResponse({'error': 'Your account is locked. Please contact support.'}, status=403)

    # Ensure the account has a password
    if not account.password:
        return JsonResponse({'error': 'Please set a password before proceeding with transactions.'}, status=403)

    # Handle POST request for transaction
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            account_number = data.get('accountNumber')
            amount = data.get('amount')
            password = data.get('password')
            beneficiary_name = data.get('accountName')
            beneficiary_address = data.get('beneficiaryAddress')
            beneficiary_bank = data.get('beneficiaryBank')
            routing_number = data.get('routingNumber')
            reason = data.get('reason')
            country = data.get('country')
            transaction_type = data.get('transactionType')

            # Validate required fields
            required_fields = [beneficiary_name, beneficiary_address, account_number,
                               beneficiary_bank, routing_number, reason, country, transaction_type]

            if not all(required_fields):
                return JsonResponse({'error': 'All required fields must be provided.'}, status=400)

            # Perform the transaction within an atomic block
            with db_transaction.atomic():
                # Check account lock again (race condition prevention)
                if account.locked:
                    return JsonResponse({'error': 'Your account is locked. Please contact support.'}, status=403)

                # Verify password
                if not account.check_password(password):
                    return JsonResponse({'error': 'Incorrect password.'}, status=400)

                # Create InternationalTransfer instance and perform transfer
                international_transfer = InternationalTransfer.objects.create(
                    beneficiary_name=beneficiary_name,  # Use the correct variable
                    beneficiary_address=beneficiary_address,
                    beneficiary_account_number=account_number,
                    beneficiary_bank=beneficiary_bank,
                    routing_number=routing_number,
                    reason=reason,
                    country=country,
                    transaction_type=transaction_type,
                    user=request.user,
                    amount=Decimal(amount),
                    updated=now()
                )

                international_transfer.transfer(amount, password)

                # Log the transaction in the Transaction model
                Transaction.objects.create(
                    wallet=account,
                    transaction_type='international_transfer',
                    to_user=beneficiary_name,
                    incoming='Debit',
                    amount=Decimal(amount),
                    updated=now()
                )

                return JsonResponse({'message': 'Transaction processed successfully.'}, status=200)

        except AccountNumber.DoesNotExist:
            logger.error("Receiver account not found.")
            return JsonResponse({'error': 'Receiver account not found.'}, status=404)

        except ValidationError as e:
            logger.error(f"Validation Error: {e}")
            return JsonResponse({'error': str(e)}, status=400)

        except Exception as e:
            logger.error(f"Unexpected error during transaction: {e}")
            return JsonResponse({'error': 'An unexpected error occurred. Please try again.'}, status=500)

    # If not a POST request, return the current balance as JSON (or handle as needed)
    return render(request, 'dashboard/international-transfer.html', {'account_balance': account_balance,
                  'account_balance_noformat': account.account_balance,
                                                                     'company_name': settings.COMPANY_NAME},)


@login_required
def transaction_history(request):
    # Set locale for currency formatting
    try:
        locale.setlocale(locale.LC_ALL, 'en_US.UTF-8')
    except locale.Error:
        locale.setlocale(locale.LC_ALL, '')

    # Retrieve or create the user's account
    account, created = AccountNumber.objects.get_or_create(user=request.user)

    # Handle account balance formatting
    try:
        account_balance = locale.currency(
            account.account_balance, grouping=True, symbol=False)
    except locale.Error:
        account_balance = f"{account.account_balance:,.2f}"

    # Filter transactions by logged-in user's wallet
    transactions = Transaction.objects.filter(wallet__user=request.user)

    # Apply the transaction filter to the queryset
    transaction_filter = TransactionFilter(request.GET, queryset=transactions)

    # Order the transactions (e.g., by `updated` in descending order)
    ordered_transactions = transaction_filter.qs.order_by('-updated')

    # Pagination logic: 10 transactions per page
    paginator = Paginator(ordered_transactions, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'filter': transaction_filter,
        'transactions': page_obj,  # Paginated and filtered transactions
        'account_balance': account_balance,
        'account_balance_noformat': account.account_balance,
        'company_name': settings.COMPANY_NAME
    }

    return render(request, 'dashboard/transaction_history.html', context)


@login_required
def account_statement(request):
    # Set locale for currency formatting
    try:
        locale.setlocale(locale.LC_ALL, 'en_US.UTF-8')
    except locale.Error:
        locale.setlocale(locale.LC_ALL, '')

    # Retrieve or create the user's account
    account, created = AccountNumber.objects.get_or_create(user=request.user)

    # Handle account balance formatting
    try:
        account_balance = locale.currency(
            account.account_balance, grouping=True, symbol=False)
    except locale.Error:
        account_balance = f"{account.account_balance:,.2f}"
    # Filter transactions by logged-in user's wallet
    transactions = Transaction.objects.filter(wallet__user=request.user)

    # Apply the transaction filter to the queryset
    transaction_filter = TransactionFilter(request.GET, queryset=transactions)

    # Order the transactions (e.g., by `updated` in descending order)
    ordered_transactions = transaction_filter.qs.order_by('-updated')

    # Pagination logic: 10 transactions per page
    paginator = Paginator(ordered_transactions, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'filter': transaction_filter,
        'transactions': page_obj,  # Paginated and filtered transactions
        'account_balance': account_balance,
        'account_balance_noformat': account.account_balance,
        'company_name': settings.COMPANY_NAME
    }

    return render(request, 'dashboard/account_statement.html', context)


def get_account_balance(request):
    try:
        # Set the locale to en_US.UTF-8
        locale.setlocale(locale.LC_ALL, 'en_US.UTF-8')
    except locale.Error:
        # Fallback to default system locale if en_US.UTF-8 fails
        locale.setlocale(locale.LC_ALL, '')

    # assuming AccountNumber model has user field
    account, created = AccountNumber.objects.get_or_create(user=request.user)

    # Format the account balance in currency format
    try:
        account_balance = locale.currency(
            account.account_balance, grouping=True, symbol=False)

        return account_balance
    except locale.Error:
        # Fallback to manual currency formatting
        account_balance = f"{account.account_balance:,.2f}"
        return account_balance


@login_required
def kyc(request):
    # Set locale for currency formatting
    try:
        locale.setlocale(locale.LC_ALL, 'en_US.UTF-8')
    except locale.Error:
        locale.setlocale(locale.LC_ALL, '')

    # Retrieve or create the user's account
    account, created = AccountNumber.objects.get_or_create(user=request.user)

    # Handle account balance formatting
    try:
        account_balance = locale.currency(
            account.account_balance, grouping=True, symbol=False)
    except locale.Error:
        account_balance = f"{account.account_balance:,.2f}"

    # Check if the account is locked
    if account.locked:
        return JsonResponse({'error': 'Your account is locked. Please contact support.'}, status=403)

    return render(request, 'dashboard/kyc.html', {'account_balance': account_balance,
                  'account_balance_noformat': account.account_balance, "page_name": "KYC", "page_message": "Your KYC has been verified.",
                                                  'company_name': settings.COMPANY_NAME},)


@login_required
def crypto(request):
    # Set locale for currency formatting
    try:
        locale.setlocale(locale.LC_ALL, 'en_US.UTF-8')
    except locale.Error:
        locale.setlocale(locale.LC_ALL, '')

    # Retrieve or create the user's account
    account, created = AccountNumber.objects.get_or_create(user=request.user)

    # Handle account balance formatting
    try:
        account_balance = locale.currency(
            account.account_balance, grouping=True, symbol=False)
    except locale.Error:
        account_balance = f"{account.account_balance:,.2f}"

    # Check if the account is locked
    if account.locked:
        return JsonResponse({'error': 'Your account is locked. Please contact support.'}, status=403)

    return render(request, 'dashboard/kyc.html', {'account_balance': account_balance,
                  'account_balance_noformat': account.account_balance, "page_name": "Crypto", "page_message": "You have no Funded or linked Crypto assets.",
                                                  'company_name': settings.COMPANY_NAME},)


@login_required
def pay_bills(request):
    # Set locale for currency formatting
    try:
        locale.setlocale(locale.LC_ALL, 'en_US.UTF-8')
    except locale.Error:
        locale.setlocale(locale.LC_ALL, '')

    # Retrieve or create the user's account
    account, created = AccountNumber.objects.get_or_create(user=request.user)

    # Handle account balance formatting
    try:
        account_balance = locale.currency(
            account.account_balance, grouping=True, symbol=False)
    except locale.Error:
        account_balance = f"{account.account_balance:,.2f}"

    # Check if the account is locked
    if account.locked:
        return JsonResponse({'error': 'Your account is locked. Please contact support.'}, status=403)

    return render(request, 'dashboard/kyc.html', {'account_balance': account_balance,
                  'account_balance_noformat': account.account_balance, "page_name": "Pay Bills", "page_message": "You have no linked bills.",
                                                  'company_name': settings.COMPANY_NAME},)


@login_required
def get_transaction_details(request, transaction_id):
    transaction = get_object_or_404(Transaction, id=transaction_id)
    data = {
        'to_user': transaction.to_user,
        'date': transaction.updated.strftime('%Y-%m-%d %H:%M'),
        'amount': float(transaction.amount),
        'account_number': transaction.wallet.account_number,
        'status': transaction.status,
    }
    return JsonResponse(data)
