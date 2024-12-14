from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from users.models import AccountNumber
from users.filters import TransactionFilter
from django.core.paginator import Paginator
from users.models import Transaction

# Create your views here.


import locale


@login_required
def dashboard(request):
    # Set the locale for formatting
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
        'filter': transaction_filter,
        'transactions': page_obj,
    }
    return render(request, 'dashboard/index.html', context)


# messages.success(request, 'Your message has been sent successfully!')
# messages.error(request, 'Your message has been sent successfully!')
# messages.warning(request, 'Your message has been sent successfully!')
# messages.info(request, 'Your message has been sent successfully!')
