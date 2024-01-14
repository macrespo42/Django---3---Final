from django.urls import path
from .views import Account, LoggedOut


urlpatterns = [
    path('', Account.as_view(), name='home'),
    path('logout/', LoggedOut.as_view(), name='logout')
]
