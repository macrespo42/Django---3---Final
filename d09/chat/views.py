from django.shortcuts import render
from django.views import View
from .models import ChatRoom


class Index(View):
    def get(self, request):
        context = {
            'chatrooms': ChatRoom.objects.values('name')
        }
        return render(request, 'chat/index.html', context)


class Room(View):
    def get(self, request):
        pass
