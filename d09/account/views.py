from django.shortcuts import render
from django.http import JsonResponse
from django.views import View
from django.contrib.auth import authenticate
from django.contrib.auth import login
from .forms import LoginForm


class Account(View):
    def get(self, request):
        context = {
                'user': request.user,
                'form': LoginForm(),
                }
        return render(request, 'account/home.html', context)

    def post(self, request):
        response = None
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')

        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            response = {
                    'code': 200,
                    'status': 'success',
                    'content': f'Logged as {user.username}'
            }
        else:
            response = {
                    'code': 401,
                    'status': 'unauthorized',
                    'content': 'incorrect username/password'
            }
        return JsonResponse(response, status=response['code'])
