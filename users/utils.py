from functools import wraps
from django.http import HttpRequest
from django.core.exceptions import PermissionDenied
from .models import AccountNumber


def check_account_locked():
    """Check if the user's account is locked"""
    def decorator(func):
        @wraps(func)
        def wrapper(request: HttpRequest, *args, **kwargs):
            # Retrieve the user's account
            try:
                account = AccountNumber.objects.get(user=request.user)
            except AccountNumber.DoesNotExist:
                raise PermissionDenied(
                    "Account not found. Please contact your bank.")

            # Check if the account is locked
            if account.locked:
                raise PermissionDenied("Account is locked, contact your bank.")

            return func(request, *args, **kwargs)
        return wrapper
    return decorator
