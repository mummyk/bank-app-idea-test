from django.urls import path
from .views import domesticTransaction, set_password, localTransaction, internationalTransaction, transaction_history, account_statement, chat_room


urlpatterns = [
    path('set/password/', set_password, name='set_password'),
    path('domestic/transfer/', domesticTransaction, name='domestic_transaction'),
    path('local/transfer/', localTransaction, name='local_transaction'),
    path('international/transfer/', internationalTransaction,
         name='international_transaction'),
    path('transaction/history/', transaction_history,
         name='transaction_history'),
    path('transaction/statement/', account_statement,
         name='account_statement'),
    path('chat/<str:room_name>/', chat_room, name='chat_room'),
]
