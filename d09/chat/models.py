from django.contrib.auth import get_user_model
from django.db import models


class Chatroom(models.Model):

    name = models.CharField(max_length=42, unique=True)


class Message(models.Model):

    author = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name="author")
    chatroom = models.ForeignKey(Chatroom, on_delete=models.CASCADE)
    content = models.TextField()
    created_ad = models.DateTimeField(auto_now_add=True)


class RoomConnectedUser(models.Model):
    chatroom = models.ForeignKey(Chatroom, on_delete=models.CASCADE)
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)

    class Meta:

        unique_together = ['chatroom', 'user']
