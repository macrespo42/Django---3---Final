from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from .models import Chatroom


@login_required(login_url="/account")
def index(request):
    context = {
        "chatrooms": Chatroom.objects.values("name")
    }
    return render(request, "chat/index.html", context)


@login_required(login_url="/account")
def room(request, name):
    return render(request, "chat/room.html", {"room_name": name})
