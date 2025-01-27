from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from users.models import AccountNumber
from users.filters import TransactionFilter
from django.core.paginator import Paginator
from users.models import Transaction
from django.http import HttpResponse

# Create your views here.


import locale


from ipware import get_client_ip


def clientIp(request):
    # Returns a tuple with IP and routability status
    client_ip, is_routable = get_client_ip(request)
    print(f"Your IP address is: {client_ip}")


def get_user_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        # The header can contain multiple IPs; take the first one
        user_ip = x_forwarded_for.split(',')[0].strip()
    else:
        user_ip = request.META.get('REMOTE_ADDR')
    return user_ip


def view_request_info(request):
    # Gather information from the request
    request_info = {
        "method": request.method,
        "path": request.path,
        "scheme": request.scheme,
        "body": request.body.decode('utf-8'),  # Decode body if necessary
        "GET": dict(request.GET),
        "POST": dict(request.POST),
        "FILES": {key: file.name for key, file in request.FILES.items()},
        "COOKIES": dict(request.COOKIES),
        "HEADERS": {key: value for key, value in request.META.items() if key.startswith('HTTP_')},
        "user": str(request.user),  # Convert user to string for representation
        # Convert session to dictionary if needed
        "session": dict(request.session),
    }

    return request_info


@login_required
def dashboard(request):
    # Set the locale for formatting
    try:
        clientIp(request)
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
    except locale.Error:
        # Fallback to manual currency formatting
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
        'title': "Dashboard",
        'account_type': account.account_type,
        'account_currency': account.account_currency,
        'account_balance': account_balance,
        'account_balance_noformat': account.account_balance,
        'filter': transaction_filter,
        'transactions': page_obj,
    }
    return render(request, 'dashboard/index.html', context)


# messages.success(request, 'Your message has been sent successfully!')
# messages.error(request, 'Your message has been sent successfully!')
# messages.warning(request, 'Your message has been sent successfully!')
# messages.info(request, 'Your message has been sent successfully!')
