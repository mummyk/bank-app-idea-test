import django_filters
from .models import Transaction


class TransactionFilter(django_filters.FilterSet):
    class Meta:
        model = Transaction
        fields = {
            # Filter by specific transaction type
            'transaction_type': ['exact'],
            'amount': ['gte', 'lte'],      # Range filtering for amount
            # Date range filtering for the updated field
            'updated': ['gte', 'lte'],
            'timestamp': ['gte', 'lte'],   # Date range filtering for timestamp
            'wallet__id': ['exact'],       # Filter by wallet ID
            # Case-insensitive filtering for beneficiary
            'to_user': ['icontains'],
        }

    # Custom ordering by 'updated' field
    order_by_updated = django_filters.OrderingFilter(
        fields=(
            ('updated', 'updated'),
        ),
        field_labels={
            'updated': 'Updated Date',
        }
    )
