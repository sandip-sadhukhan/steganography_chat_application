from django.shortcuts import render, HttpResponse, redirect
from django.contrib.auth import login as auth_login, logout as auth_logout, authenticate
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.decorators import login_required

def home(request):
    return render(request, 'pages/home.html')


def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            auth_login(request, user)
            messages.add_message(request, messages.SUCCESS, 'Logged in successfully.')
            return redirect('/dashboard')
        else:
            messages.add_message(request, messages.ERROR, 'Credentials not correct.')
            return redirect('/login')
    return render(request, 'pages/login.html')

def signup(request):
    if request.method == 'POST':
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']

        user = User.objects.create_user(
            first_name=first_name,
            last_name=last_name,
            username=username,
            email=email,
            password=password
        )

        user = authenticate(request, username=username, password=password)
        if user is not None:
            auth_login(request, user)
            messages.add_message(request, messages.SUCCESS, 'Signed up successfully.')
            return redirect('/dashboard')
        else:
            messages.add_message(request, messages.ERROR, 'Credentials not correct.')
            return redirect('/signup')

    return render(request, 'pages/signup.html')

def logout(request):
    auth_logout(request)
    return redirect("/login")

@login_required
def dashboard(request):
    return render(request, 'pages/dashboard.html')


@login_required
def chat(request):
    return render(request, 'pages/chat.html')
