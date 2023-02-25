import json

from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer


class NotificationsWorker(WebsocketConsumer):
    user_id = None
    room_group_name = 'notifications_admin'

    def connect(self):
        # get user id from url
        self.user_id = self.scope['url_route']['kwargs']['user_id']

        self.room_group_name = 'notifications_%s' % self.user_id

        if self.user_id is not None and self.user_id != "None":
            self.accept()
            return
        else:
            print("User id is None")

        self.accept()

    def disconnect(self, close_code):
        self.close()

    def send_chat_message(self, event):
        message = event['message']

        # Send message to WebSocket
        self.send(text_data=json.dumps({
            'message': message
        }))

    def send_new_notifications(self, notification):
        user_id = notification.user
        print(user_id)
        # serialise notification
        notification = {
            'id': notification.id,
            'message': notification.message,
            'user': notification.user,
            'created_at': notification.created_at.strftime('%Y-%m-%d %H:%M:%S'),
            'opened': notification.opened,
            'type': notification.type,
        }

        # send notification to user
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                'type': 'send_chat_message',
                'message': notification
            }
        )
