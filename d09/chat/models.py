from django.db import models


class ChatRoom(models.Model):
    name = models.CharField(max_length=42, unique=True)


class Message(models.Model):
    content = models.TextField()
    room = models.ForeignKey(ChatRoom, on_delete=models.CASCADE)
