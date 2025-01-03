from django.urls import path
from user.consumers import OnlineStatusConsumer, PingConsumer

websocket_urlpatterns = [
    path('/user/ping/', PingConsumer.as_asgi()),
    path('/user/online-status/', OnlineStatusConsumer.as_asgi()),
]
