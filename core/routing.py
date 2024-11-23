# your_app_name/routing.py

from django.urls import path
from core import customers   # Import your consumer class

websocket_urlpatterns = [
    # Define WebSocket path
    path('ws/chat/<str:room_name>/', customers.ChatConsumer.as_asgi()),
]
