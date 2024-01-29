from django.shortcuts import render

from .models import Chatroom


def index(request):
    context = {
        "chatrooms": Chatroom.objects.values("name")
    }
    return render(request, "chat/index.html", context)


def room(request, name):
    return render(request, "chat/room.html", {"room_name": name})
