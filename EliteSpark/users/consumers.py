import json

from channels.db import database_sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer
from django.contrib.auth.models import User
from .models import Notification


class NotificationConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.user_id = self.scope['url_route']['kwargs']['user_id']
        self.channel_name = 'notification_%s' % self.user_id

        # Join room group
        await self.channel_layer.group_add(
            self.user_id,
            self.channel_name
        )
        await self.accept()

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(
            self.user_id,
            self.channel_name
        )

    # Receive message from WebSocket
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)

        if await self.user_check(text_data_json['user-id']) != 0:
            if text_data_json['process'] == 'unopened_notifications_count':
                un_seen_notice = await self.notification_check(text_data_json['user-id'])
                friend_notice = await self.friend_notifications(text_data_json['user-id'])
                await self.send(json.dumps({
                    'process': 'unopened_notifications_count',
                    'status': True,
                    'count': un_seen_notice,
                    'friend_notice_count': friend_notice
                }))
            else:
                await self.send(json.dumps({
                    'process': 'No mentioned',
                    'status': True,
                }))

    # Receive message from room group
    async def notification_send(self, event):
        print(event)
        await self.send("Working...")

    @database_sync_to_async
    def user_check(self, user_id):
        return User.objects.filter(id=user_id).count()

    @database_sync_to_async
    def notification_check(self, user_id):
        user = User.objects.get(id=user_id)
        return Notification.objects.filter(notify_receiver=user).filter(is_seen=False).count()

    @database_sync_to_async
    def friend_notifications(self, user_id):
        user = User.objects.get(id=user_id)
        return Notification.objects.filter(notify_receiver=user).filter(message='Friend Request').count()
