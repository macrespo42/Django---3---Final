import json

from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer


class ChatConsumer(WebsocketConsumer):
    def connect(self):
        self.room_name = self.scope["url_route"]["kwargs"]["room_name"]
        self.room_group_name = f"chat_{self.room_name}"

        # Join room group
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name, self.channel_name
        )

        # Get the username of the user joining the room
        username = self.scope.get("user", None)
        if username:
            username = username.username
            # Send a special message when a user joins the room
            self.send_special_message(f"{username} joined the room")

        self.accept()

    def disconnect(self, _):
        # Leave room group
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name, self.channel_name
        )

    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json["message"]

        # Send message to room group
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name, {"type": "chat.message", "message": message}
        )

    def chat_message(self, event):
        message = event["message"]

        # Send message to WebSocket
        self.send(text_data=json.dumps({"message": message}))

    def send_special_message(self, message):
        # Send a special message to the room group
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name, {"type": "chat.special_message", "message": message}
        )

    def chat_special_message(self, event):
        # Handle special messages (e.g., user joined the room)
        message = event["message"]

        # Send the special message to WebSocket
        self.send(text_data=json.dumps({"message": message}))
