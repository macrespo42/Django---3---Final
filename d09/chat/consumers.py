import json

from channels.db import database_sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer

from .models import Chatroom, Message


class ChatConsumer(AsyncWebsocketConsumer):
    @database_sync_to_async
    def get_last_messages(self):
        last_messages = Message.objects.filter(chatroom__name=self.room_name).order_by("-created_ad").values("content")[:3]
        return [message for message in last_messages]

    @database_sync_to_async
    def create_chat(self, content, author):
        chatroom = Chatroom.objects.get(name=self.room_name)
        return Message.objects.create(author=author, chatroom=chatroom, content=content)

    async def connect(self):
        self.room_name = self.scope["url_route"]["kwargs"]["room_name"]
        self.room_group_name = f"chat_{self.room_name}"

        # Join room group
        await self.channel_layer.group_add(
            self.room_group_name, self.channel_name
        )

        # Get the username of the user joining the room
        username = self.scope.get("user", None)
        if username:
            username = username.username
            # Send a special message when a user joins the room
            await self.send_special_message(f"{username} joined the room")

        await self.accept()

    async def disconnect(self, _):
        username = self.scope.get("user", None)
        if username:
            username = username.username
            # Send a special message when a user joins the room
            await self.send_special_message(f"{username} leave the room")
        # Leave room group
        await self.channel_layer.group_discard(
            self.room_group_name, self.channel_name
        )

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json["message"]

        # Send message to room group
        await self.channel_layer.group_send(
            self.room_group_name, {"type": "chat.message", "message": message}
        )

    async def chat_message(self, event):
        message = event["message"]

        user = self.scope.get("user", None)
        if user:
            await self.create_chat(message, user)

        # Send message to WebSocket
        await self.send(text_data=json.dumps({"message": message}))

    async def send_special_message(self, message):
        # Send a special message to the room group
        await self.channel_layer.group_send(
            self.room_group_name, {"type": "chat.special_message", "message": message}
        )

    async def chat_special_message(self, event):
        # Handle special messages (e.g., user joined the room)

        message = event["message"]

        messages_historic = await self.get_last_messages()
        if messages_historic:
            messages_historic.reverse()
        for old_message in messages_historic:
            await self.send(text_data=json.dumps({"message": old_message['content']}))

        # Send the special message to WebSocket
        await self.send(text_data=json.dumps({"message": message}))
