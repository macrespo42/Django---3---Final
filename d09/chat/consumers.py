import json

from channels.db import database_sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer

from .models import Chatroom, Message, RoomConnectedUser


class ChatConsumer(AsyncWebsocketConsumer):
    @database_sync_to_async
    def create_chat(self, content, author):
        chatroom = Chatroom.objects.get(name=self.room_name)
        return Message.objects.create(author=author, chatroom=chatroom, content=content)

    @database_sync_to_async
    def add_connected_user(self, user):
        chatroom = Chatroom.objects.get(name=self.room_name)
        RoomConnectedUser.objects.create(user=user, chatroom=chatroom)

    @database_sync_to_async
    def remove_connected_user(self, user):
        chatroom = Chatroom.objects.get(name=self.room_name)
        RoomConnectedUser.objects.get(user=user, chatroom=chatroom).delete()

    async def connect(self):
        self.room_name = self.scope["url_route"]["kwargs"]["room_name"]
        self.room_group_name = f"chat_{self.room_name}"

        # Join room group
        await self.channel_layer.group_add(
            self.room_group_name, self.channel_name
        )

        # Get the username of the user joining the room
        user = self.scope.get("user", None)
        if user:
            # Send a special message when a user joins the room
            await self.send_special_message(f"{user.username} joined the room")

            await self.add_connected_user(user)

        await self.accept()

    async def disconnect(self, _):
        user = self.scope.get("user", None)
        if user:
            # Send a special message when a user joins the room
            await self.send_special_message(f"{user.username} leave the room")

            await self.remove_connected_user(user)
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

        # Send the special message to WebSocket
        await self.send(text_data=json.dumps({"message": message}))
