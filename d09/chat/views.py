from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from .models import Chatroom, Message


@login_required(login_url="/account")
def index(request):
    context = {
        "chatrooms": Chatroom.objects.values("name")
    }
    return render(request, "chat/index.html", context)


@login_required(login_url="/account")
def room(request, name):
    messages = Message.objects.filter(chatroom__name=name).order_by("created_ad").values("content")
    context = {
        "room_name": name,
        "message_historic": messages[len(messages) - 3:]
    }
    return render(request, "chat/room.html", context)
