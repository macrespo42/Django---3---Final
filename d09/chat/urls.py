from django.urls import path
from .views import Index, Room

urlpatterns = [
    path('', Index.as_view(), name='chat-index'),
    path('<str:name>/', Room.as_view(), name='chatroom'),
]
