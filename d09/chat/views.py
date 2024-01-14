from django.shortcuts import render, get_object_or_404
from django.views import View
from .models import ChatRoom


class Index(View):
    def get(self, request):
        context = {
            'chatrooms': ChatRoom.objects.values('name')
        }
        return render(request, 'chat/index.html', context)


class Room(View):
    def get(self, request, name=None):
        room = get_object_or_404(ChatRoom, name=name)
        context = {
                'room': room
        }
        return render(request, 'chat/chat.html', context)
