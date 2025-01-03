import json
from channels.generic.websocket import AsyncWebsocketConsumer
from asgiref.sync import sync_to_async
from django.contrib.auth.models import AnonymousUser

from user.constants import MessageType
from user.models import Profile
from utils.consumer_response import ConsumerResponse

ONLINE_USERS_GROUP = 'online_users'

class OnlineStatusConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        user = self.scope['user']
        if user is AnonymousUser and not user.is_authenticated:
            await self.close()
        else:
            await self.channel_layer.group_add(ONLINE_USERS_GROUP, self.channel_name)
            await self.update_user_activity(user)
            await self.accept()

    async def disconnect(self, close_code):
        if self.scope['user'].is_authenticated:
            user = self.scope['user']
            await self.channel_layer.group_discard(ONLINE_USERS_GROUP, self.channel_name)
            await self.set_user_offline(user)

    async def receive(self, text_data=None, bytes_data=None):
        data = json.loads(text_data)

        msg_type = data['type']
        user = self.scope['user']

        match msg_type:
            case MessageType.CHECK_STATUS.value:
                is_online = await self.check_user_online(user)
                await self.send(text_data=json.dumps(ConsumerResponse(data = {'is_online': is_online, 'type': msg_type})))
            case MessageType.UPDATE_ONLINE_STATUS.value:
                await self.update_user_activity(user)
                await self.send(text_data=json.dumps(ConsumerResponse(data= {'is_online': True, 'type': msg_type})))
            case _:
                await self.send(text_data=json.dumps(ConsumerResponse(status= 'error', message= 'invalid message type', data = {'type': MessageType.ERROR.value})))

    @sync_to_async
    def update_user_activity(self, user):
        print('update_user_activity', user)
        user_profile = Profile.objects.get(user=user)
        user_profile.update_last_activity()

    @sync_to_async
    def set_user_offline(self, user):
        print('set_user_offline', user)
        user_profile = Profile.objects.get(user=user)
        user_profile.set_offline()

    @sync_to_async
    def check_user_online(self, user):
        user_profile = Profile.objects.get(user=user)
        return user_profile.is_online()


class PingConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.accept()

    async def receive(self, text_data=None, bytes_data=None):
        data = json.loads(text_data)
        await self.send(text_data=json.dumps(data))

    async def disconnect(self, close_code):
        await self.close()
