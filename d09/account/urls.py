from django.urls import path
from .views import Account


urlpatterns = [
    path('', Account.as_view(), name='home'),
]
