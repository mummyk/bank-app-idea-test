from .filters import TransactionFilter
import logging
from decimal import Decimal
from django.utils.timezone import now
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from django.db import transaction as db_transaction  # Ensure atomic transactions
from .models import Transaction, DomesticTransfer, AccountNumber, LocalTransfer, InternationalTransfer, Profile
from .forms import DomesticTransferForm, LocalTransferForm, InternationalTransferForm
from .forms import ProfileForm, Profile_pictureForm, ProfileFormLite
from .utils import check_account_locked

# Initialize a logger for error tracking
logger = logging.getLogger(__name__)


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


# Update or add Profile Picture
@login_required
def manage_profile_image(request):
    # Get the user's profile or create one if it doesn't exist
    profile, created = Profile.objects.get_or_create(user=request.user)
    profile_picture_url = ''
    if profile.profile_picture:
        profile_picture_url = request.build_absolute_uri(
            profile.profile_picture.url)

    if request.method == 'POST':
        form = Profile_pictureForm(
            request.POST, request.FILES, instance=profile)
        if form.is_valid():
            # Update user first name and last name
            form.save()  # Save profile data
            messages.success(
                request, 'Your profile picture has been updated successfully!')
            # log_action(request.user, ADDITION, f"Added profile_picture for {
            #     request.user.username}", profile)

            # Redirect to a profile view or another page
            return redirect('profile')
    else:
        messages.error(
            request, 'Can not update your profile picture!')

        # log_action(request.user, ADDITION, f"Try adding profile_picture for {
        #     request.user.username}", profile)
        form = ProfileForm(instance=profile)

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

    profile_picture_url = request.build_absolute_uri(
        profile.profile_picture.url) if profile.profile_picture else ""

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
# @check_account_locked()  # Apply the account lock check decorator
def domesticTransaction(request):
    try:
        # Retrieve the user's account
        account = AccountNumber.objects.get(user=request.user)

        # Check if the user has set a password
        if not account.password:
            messages.warning(
                request, "You need to set a password before proceeding with transactions."
            )
            # Redirect to the password setup page
            return redirect(reverse('set_password'))

    except AccountNumber.DoesNotExist:
        messages.error(
            request, "Your account could not be found. Please contact customer support."
        )
        return redirect('home')  # Redirect to a home or error page

    if request.method == 'POST':
        form = DomesticTransferForm(request.POST)
        if form.is_valid():
            try:
                with db_transaction.atomic():
                    # Perform the transfer operation
                    transfer_data = form.cleaned_data
                    amount = transfer_data['amount']
                    beneficiary = transfer_data['beneficiary']
                    password = request.POST.get('password')

                    if account.locked:
                        messages.warning(
                            request, """your account has been locked, please contact customer support or use the live chat below."""
                        )
                        # Redirect to the password setup page
                        return redirect(reverse('domestic_transaction'))

                    # Ensure the transfer is valid
                    if not account.check_password(password):
                        messages.error(request, "Incorrect password.")
                        return render(request, 'dashboard/domestic-transfer.html', {'form': form})

                    # Create a DomesticTransfer instance
                    domestic_transfer = DomesticTransfer.objects.create(
                        user=request.user,
                        beneficiary=beneficiary,
                        amount=Decimal(amount),
                        updated=now()  # Set the current datetime for `updated`
                    )

                    # Deduct the amount from the user's account balance
                    domestic_transfer.transfer(amount, password)

                    # Log the transaction in the Transaction model
                    Transaction.objects.create(
                        wallet=account,
                        transaction_type='domestic_transfer',
                        to_user=beneficiary,  # Adjust if the beneficiary is also a user
                        incoming='Debit',
                        amount=Decimal(amount),
                        updated=now()  # Set the current datetime for `updated`
                    )

                    messages.success(
                        request, 'Transaction created successfully.')
                    return redirect('dashboard')

            except Exception as e:
                logger.error(f"Error saving transaction: {e}")
                messages.error(
                    request, f'An unexpected error occurred, {e}')

        else:
            # Collect and log form errors for debugging
            logger.error(f"Form submission errors: {form.errors.as_json()}")
            messages.error(request, 'Please correct the errors below.')
    else:
        form = DomesticTransferForm()

    return render(request, 'dashboard/domestic-transfer.html', {'form': form})


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
    try:
        # Retrieve the user's account
        account = AccountNumber.objects.get(user=request.user)

        # Check if the user has set a password
        if not account.password:
            messages.warning(
                request, "You need to set a password before proceeding with transactions."
            )
            return redirect(reverse('set_password'))

    except AccountNumber.DoesNotExist:
        messages.error(
            request, "Your account could not be found. Please contact customer support."
        )
        return redirect('home')

    if request.method == 'POST':
        form = LocalTransferForm(request.POST)
        if form.is_valid():
            try:
                with db_transaction.atomic():
                    # Perform the transfer operation
                    transfer_data = form.cleaned_data
                    amount = transfer_data['amount']
                    beneficiary_bank = transfer_data['beneficiary_bank']
                    account_number = transfer_data['beneficiary_account_number']
                    transaction_type = transfer_data['transaction_type']
                    password = request.POST.get('password')

                    # Check if the account is locked
                    if account.locked:
                        messages.warning(
                            request, "Your account is locked. Please contact customer support."
                        )
                        return redirect(reverse('local_transaction'))

                    # Validate the password
                    if not account.check_password(password):
                        messages.error(request, "Incorrect password.")
                        return render(request, 'dashboard/local-transfer.html', {'form': form})

                    # Create the LocalTransfer instance
                    local_transfer = LocalTransfer.objects.create(
                        user=request.user,
                        beneficiary_bank=beneficiary_bank,
                        beneficiary_account_number=account_number,
                        transaction_type=transaction_type,
                        amount=Decimal(amount),
                        updated=now()
                    )

                    # Deduct the amount and perform the transfer
                    local_transfer.transfer(amount, password)

                    # Log the transaction in the Transaction model
                    Transaction.objects.create(
                        wallet=account,
                        transaction_type='local_transfer',
                        to_user=beneficiary_bank,  # Adjust if beneficiary is a user
                        incoming='Debit',
                        amount=Decimal(amount),
                        updated=now()
                    )

                    messages.success(
                        request, "Transaction processed successfully."
                    )
                    return redirect('dashboard')

            except Exception as e:
                logger.error(f"Error during local transaction: {e}")
                messages.error(
                    request, f"An unexpected error occurred: {e}"
                )

        else:
            # Log form errors
            logger.error(f"Form errors: {form.errors.as_json()}")
            messages.error(request, "Please correct the errors below.")
    else:
        form = LocalTransferForm()

    return render(request, 'dashboard/local-transfer.html', {'form': form})


@login_required
def internationalTransaction(request):
    try:
        # Retrieve the user's account
        account = AccountNumber.objects.get(user=request.user)

        # Check if the user has set a password
        if not account.password:
            messages.warning(
                request, "You need to set a password before proceeding with transactions."
            )
            return redirect(reverse('set_password'))

    except AccountNumber.DoesNotExist:
        messages.error(
            request, "Your account could not be found. Please contact customer support."
        )
        return redirect('home')

    if request.method == 'POST':
        form = InternationalTransferForm(request.POST)
        if form.is_valid():
            try:
                with db_transaction.atomic():
                    # Perform the transfer operation
                    transfer_data = form.cleaned_data
                    amount = transfer_data['amount']
                    beneficiary_bank = transfer_data['beneficiary_bank']
                    beneficiary_name = transfer_data['beneficiary_name']
                    beneficiary_address = transfer_data['beneficiary_address']
                    beneficiary_account_number = transfer_data['beneficiary_account_number']
                    routing_number = transfer_data['routing_number']
                    reason = transfer_data['reason']
                    country = transfer_data['country']
                    transaction_type = transfer_data['transaction_type']
                    password = request.POST.get('password')

                    # Check if the account is locked
                    if account.locked:
                        messages.warning(
                            request, "Your account is locked. Please contact customer support."
                        )
                        return redirect(reverse('international_transaction'))

                    # Validate the password
                    if not account.check_password(password):
                        messages.error(request, "Incorrect password.")
                        return render(request, 'dashboard/international-transfer.html', {'form': form})

                    # Create the internationalTransfer instance
                    international_transfer = InternationalTransfer.objects.create(
                        beneficiary_name=beneficiary_name,
                        beneficiary_address=beneficiary_address,
                        beneficiary_account_number=beneficiary_account_number,
                        beneficiary_bank=beneficiary_bank,
                        routing_number=routing_number,
                        reason=reason,
                        country=country,
                        transaction_type=transaction_type,
                        user=request.user,
                        amount=Decimal(amount),
                        updated=now()
                    )

                    # Deduct the amount and perform the transfer
                    international_transfer.transfer(amount, password)

                    # Log the transaction in the Transaction model
                    Transaction.objects.create(
                        wallet=account,
                        transaction_type='international_transfer',
                        to_user=beneficiary_bank,  # Adjust if beneficiary is a user
                        incoming='Debit',
                        amount=Decimal(amount),
                        updated=now()
                    )

                    messages.success(
                        request, "Transaction processed successfully."
                    )
                    return redirect('dashboard')

            except Exception as e:
                logger.error(f"Error during international transaction: {e}")
                messages.error(
                    request, f"An unexpected error occurred: {e}"
                )

        else:
            # Log form errors
            logger.error(f"Form errors: {form.errors.as_json()}")
            messages.error(request, "Please correct the errors below.")
    else:
        form = InternationalTransferForm()

    return render(request, 'dashboard/international-transfer.html', {'form': form})


@login_required
def transaction_history(request):
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
    }

    return render(request, 'dashboard/transaction_history.html', context)


@login_required
def account_statement(request):
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
    }

    return render(request, 'dashboard/account_statement.html', context)
