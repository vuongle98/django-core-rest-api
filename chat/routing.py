from . import consumer
from django.urls.conf import path

websocket_urlpatterns = [
    path('ws/chat/<str:room_name>/', consumer.ChatConsumer.as_asgi()),
    # path('ws/personal_chat/<str:room_name>/', consumer.PersonalConsumer.as_asgi()),
]