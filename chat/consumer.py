# consumers.py
import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from datetime import datetime

from django.core.exceptions import ObjectDoesNotExist

from chat.models import Room, ChatMessage
from user.models import CoreUser

MESSAGE_MAX_LENGTH = 100

MESSAGE_ERROR_TYPE = {
    "MESSAGE_OUT_OF_LENGTH": 'MESSAGE_OUT_OF_LENGTH',
    "UN_AUTHENTICATED": 'UN_AUTHENTICATED',
    "INVALID_MESSAGE": 'INVALID_MESSAGE',
}

MESSAGE_TYPE = {
    "WENT_ONLINE": 'WENT_ONLINE',
    "WENT_OFFLINE": 'WENT_OFFLINE',
    "IS_TYPING": 'IS_TYPING',
    "NOT_TYPING": 'NOT_TYPING',
    "MESSAGE_COUNTER": 'MESSAGE_COUNTER',
    "OVERALL_MESSAGE_COUNTER": 'OVERALL_MESSAGE_COUNTER',
    "TEXT_MESSAGE": 'TEXT_MESSAGE',
    "MESSAGE_READ": 'MESSAGE_READ',
    "ALL_MESSAGE_READ": 'ALL_MESSAGE_READ',
    "ERROR_OCCURRED": 'ERROR_OCCURRED'
}


class ChatConsumer(AsyncWebsocketConsumer):

    def __init__(self, *args, **kwargs):
        super().__init__(args, kwargs)
        self.user = None
        self.room_group_name = None
        self.room_name = None

    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = self.room_name
        self.user = self.scope['user']

        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        if self.scope["user"].is_authenticated:
            print(self.user, "is authenticated")
            await self.accept()
        else:
            print(self.user, "not authenticated")
            await self.accept()
            await self.send(text_data=json.dumps({
                "msg_type": MESSAGE_TYPE['ERROR_OCCURRED'],
                "error_message": MESSAGE_ERROR_TYPE["UN_AUTHENTICATED"],
                "user": self.user.username,
            }))
            await self.close(code=4001)

    async def disconnect(self, code):
        print(self.user, "disconnect")
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    # Receive message from WebSocket
    async def receive(self, text_data):
        data = json.loads(text_data)
        message = data.get('message')
        msg_type = data.get('msg_type')
        username = data.get('username')
        room_name = data.get('room_name')

        print(message, msg_type, username)

        if msg_type == MESSAGE_TYPE['TEXT_MESSAGE']:
            if len(message) <= MESSAGE_MAX_LENGTH:
                # msg_id = uuid.uuid4()
                await self.channel_layer.group_send(
                    self.room_group_name,
                    {
                        'type': 'chat_message',
                        'message': message,
                        'username': username
                    }
                )
                await self.save_text_message(room_name, username, message)
                # await self.channel_layer.group_send(
                #     f'personal__{current_user_id}',
                #     {
                #         'type': 'message_counter',
                #         'user_id': self.user.id,
                #         'current_user_id': current_user_id
                #     }
                # )
            else:
                await self.send(text_data=json.dumps({
                    'msg_type': MESSAGE_TYPE['ERROR_OCCURRED'],
                    'error_message': MESSAGE_ERROR_TYPE["MESSAGE_OUT_OF_LENGTH"],
                    'message': message,
                    'username': username,
                    'timestamp': str(datetime.now()),
                }))
        elif msg_type == MESSAGE_TYPE['MESSAGE_READ']:
            msg_id = data['msg_id']
            await self.msg_read(msg_id)
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'msg_read',
                    'msg_id': msg_id,
                    'username': username
                }
            )
        elif msg_type == MESSAGE_TYPE['ALL_MESSAGE_READ']:
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'all_msg_read',
                    'username': username,
                }
            )
            await self.read_all_msg(self.room_name[5:], username)
        elif msg_type == MESSAGE_TYPE['IS_TYPING']:
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'user_is_typing',
                    'username': username,
                }
            )
        elif msg_type == MESSAGE_TYPE["NOT_TYPING"]:
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'user_not_typing',
                    'username': username,
                }
            )
        elif msg_type == MESSAGE_TYPE['MESSAGE_COUNTER']:
            msg_count = 100
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'message_counter',
                    'username': username,
                    'counter': msg_count
                }
            )

    # Receive message from room group
    async def chat_message(self, event):
        await self.send(text_data=json.dumps({
            'msg_type': MESSAGE_TYPE['TEXT_MESSAGE'],
            'message': event['message'],
            'username': event['username'],
            'timestamp': str(datetime.now())
        }))

    async def msg_as_read(self, event):
        await self.send(text_data=json.dumps({
            'msg_type': MESSAGE_TYPE['MESSAGE_READ'],
            'username': event['username']
        }))

    async def all_msg_read(self, event):
        await self.send(text_data=json.dumps({
            'msg_type': MESSAGE_TYPE['ALL_MESSAGE_READ'],
            'username': event['username']
        }))

    async def user_is_typing(self, event):
        await self.send(text_data=json.dumps({
            'msg_type': MESSAGE_TYPE['IS_TYPING'],
            'username': event['username']
        }))

    async def user_not_typing(self, event):
        await self.send(text_data=json.dumps({
            'msg_type': MESSAGE_TYPE['NOT_TYPING'],
            'username': event['username']
        }))

    async def message_counter(self, event):
        await self.send(text_data=json.dumps({
            'msg_type': MESSAGE_TYPE['MESSAGE_COUNTER'],
            'username': event['username'],
            'counter': event['counter']
        }))

    @database_sync_to_async
    def save_text_message(self, room_name, username, message):
        sender = CoreUser.objects.get(username=username)
        try:
            room = Room.objects.get(name=room_name)
        except ObjectDoesNotExist:
            room = Room.objects.create(name=room_name, creator=sender, type='GROUP')
            room.participants.add(sender)
            room.save()
        return ChatMessage.objects.create(
            sender=sender, content=message,
            room=room
        ).save()

    @database_sync_to_async
    def msg_read(self, msg_id):
        return ChatMessage.message_read_true(msg_id)

    @database_sync_to_async
    def read_all_msg(self, room_id, user):
        return ChatMessage.all_msg_read(room_id, user)