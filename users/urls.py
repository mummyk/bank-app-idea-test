from django.urls import path
from .views import domesticTransaction, set_password, localTransaction, internationalTransaction, transaction_history, account_statement, manage_profile, user_profile, manage_profile_image, delete_profile_image, check_receiver, kyc, crypto, pay_bills, get_transaction_details


urlpatterns = [
    path('set/password/', set_password, name='set_password'),
    path('check-account/<str:account_number>/',
         check_receiver, name='check_account'),
    path('domestic/transfer/', domesticTransaction, name='domestic_transaction'),
    path('local/transfer/', localTransaction, name='local_transaction'),
    path('international/transfer/', internationalTransaction,
         name='international_transaction'),
    path('get-transaction-details/<int:transaction_id>/',
         get_transaction_details, name='get_transaction_details'),
    path('kyc/', kyc, name='kyc'),
    path('crypto/', crypto, name='crypto'),
    path('pay-bills/', pay_bills, name='pay_bills'),
    path('transaction/history/', transaction_history,
         name='transaction_history'),
    path('transaction/statement/', account_statement,
         name='account_statement'),
    path('profile/manage/', manage_profile, name='manage_profile'),
    path('profile/manage/images/', manage_profile_image,
         name='manage_profile_images'),
    path('profile/delete/', delete_profile_image, name='delete_profile_image'),
    path('profile/', user_profile, name='profile'),
]
