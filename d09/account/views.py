from django.shortcuts import render
from .forms import LoginForm


def home(request):
    context = {'user': request.user}
    if not request.user.is_authenticated:
        context['form'] = LoginForm()
    return render(request, 'account/home.html', context)
