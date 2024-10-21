from django.urls import re_path

from chat.consumer import ChatConsumer
from .consumer import EchoConsumer

websocket_urlpatterns = [
    re_path(r"^ws/echo/$", EchoConsumer.as_asgi()),
    re_path(r"^ws/chat/(?P<room_name>\w+)/$", ChatConsumer.as_asgi()),
]