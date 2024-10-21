# notifications/consumers.py

import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async

class UserConsumer(AsyncWebsocketConsumer):
    users_online = set()  # In-memory storage for online users

    async def connect(self):

        self.user = self.scope['user']
        if self.user.is_authenticated:
            # Mark user as online
            await self.set_user_status(True)

            # Add user to the in-memory online users set
            self.users_online.add(self.user.id)

            # Join the WebSocket group
            self.room_group_name = f"user_{self.user.id}_status"
            await self.channel_layer.group_add(
                self.room_group_name,
                self.channel_name
            )

            # Accept WebSocket connection
            await self.accept()
        else:
            # Reject the WebSocket connection if not authenticated
            await self.close()

    async def disconnect(self, close_code):
        if self.user.is_authenticated:
            # Remove user from online status
            await self.set_user_status(False)

            # Remove user from in-memory online users set
            self.users_online.discard(self.user.id)

            # Leave the group
            await self.channel_layer.group_discard(
                self.room_group_name,
                self.channel_name
            )

    @database_sync_to_async
    async def set_user_status(self, status):
        """
        Set the user's status as online (True) or offline (False)
        """
        # user_status, created = UserStatus.objects.get_or_create(user=self.user)
        # user_status.online = status
        # user_status.save()

        print("user status " + str(status))

    async def receive(self, text_data):
        # Handle incoming messages (if needed)
        data = json.loads(text_data)
        message = data.get('message', '')

        # Broadcast the message to the group (could be for notifications)
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'send_message',
                'message': message
            }
        )

    async def send_message(self, event):
        message = event['message']

        # Send the message to WebSocket
        await self.send(text_data=json.dumps({
            'message': message
        }))
