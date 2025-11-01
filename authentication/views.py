from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.contrib.auth import logout, login
from django.contrib import messages


# Create your views here.

def index(request):
    return render(request, 'index.html')

def login_view(request):
    if request.method == 'POST':
        username = (request.POST.get('username') or '').strip()
        password = (request.POST.get('password') or '').strip()

        # check if users have entered correct credentials
        user = authenticate(username=username, password=password)

        if user is not None:
            login(request, user)
            next_url = request.GET.get('next') or request.POST.get('next')
            return redirect(next_url or 'home')
        else:
            messages.error(request, 'Invalid username or password')
            return render(request, 'login.html', status=401)

    return render(request, 'login.html')

def logout_view(request):
    logout(request)
    return redirect("login")