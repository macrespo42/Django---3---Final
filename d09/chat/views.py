from django.shortcuts import get_object_or_404, redirect, render
from django.views import View

from .models import ChatRoom, Message


class Index(View):
    def get(self, request):
        if not request.user.is_authenticated:
            return redirect('home')
        context = {
            'chatrooms': ChatRoom.objects.values('name')
        }
        return render(request, 'chat/index.html', context)


class Room(View):
    def get(self, request, name=None):
        if not request.user.is_authenticated:
            return redirect('home')
        room = get_object_or_404(ChatRoom, name=name)
        messages = Message.objects.filter(
            room__pk=room.pk).values('content', 'author')
        context = {
            'room': room,
            'messages': messages,
        }
        return render(request, 'chat/chat.html', context)
