import json
from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
from .models import ChatMessage
from django.contrib.auth.models import User


class ChatConsumer(WebsocketConsumer):
    def connect(self):
        user1_id = int(self.scope["url_route"]["kwargs"]["user1"])
        user2_id = int(self.scope["url_route"]["kwargs"]["user2"])
        room = f"chat_{user1_id}_{user2_id}"
        self.room_name = room
        self.room_group_name = room
        user = self.scope["user"]
        if user is not None:
            # Authorization
            if user.id == user1_id or user.id == user2_id:
                async_to_sync(self.channel_layer.group_add)(
                    self.room_group_name, self.channel_name
                )
                self.accept()

    def disconnect(self, close_code):
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name, self.channel_name
        )

    def receive(self, text_data):
        data = json.loads(text_data)
        # print(data)

        """
        data = {
            'type': 'fetch_messages/send_message',
            'sender': '3',
            'receiver': '2', # userid
            'message': 'Hello!',
            'fileURL': '/media/hello.jpg' # if any,
            'steganographyImage': True/False,
            'passwordProtectedSteganographyImage': True/False
        }
        """
        user1_id = int(self.scope["url_route"]["kwargs"]["user1"])
        user2_id = int(self.scope["url_route"]["kwargs"]["user2"])
        user = self.scope["user"]

        sender = user
        receiver = None
        if user.id == user1_id:
            receiver = User.objects.get(id=user2_id)
        elif user.id == user2_id:
            receiver = User.objects.get(id=user1_id)


        if data["type"] == "fetch_messages":
            self.send(
                text_data=json.dumps(
                    {
                        "type": "fetch_messages",
                        "messages": ChatMessage.get_messages(sender, receiver),
                    }
                )
            )
        elif data["type"] == "send_message":
            steganographyImage = data.get('steganographyImage', False)
            passwordProtectedSteganographyImage = data.get('passwordProtectedSteganographyImage', False)

            # create message object
            msg = ChatMessage.objects.create(
                sender=sender,
                receiver=receiver,
                message=data.get("message"),
                fileURL=data.get("fileURL"),
                steganographyImage= steganographyImage,
                passwordProtectedSteganographyImage=passwordProtectedSteganographyImage
            )
            async_to_sync(self.channel_layer.group_send)(
                self.room_group_name, {"type": "send_data", "data": msg.serialize()}
            )

    def send_data(self, event):
        data = event["data"]
        self.send(text_data=json.dumps({"type": "send_message", "message": data}))
