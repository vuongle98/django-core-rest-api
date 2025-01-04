from . import consumer
from django.urls.conf import path

websocket_urlpatterns = [
    path('/chat/<str:room_name>/', consumer.ChatConsumer.as_asgi())
]