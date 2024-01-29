from django.urls import path

from .views import index, room

urlpatterns = [
    path("", index, name="chat-home"),
    path("<str:name>/", room, name="chatroom")
]
