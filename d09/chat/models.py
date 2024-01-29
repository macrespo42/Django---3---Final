from django.db import models


class Chatroom(models.Model):

    name = models.CharField(max_length=42, unique=True)
