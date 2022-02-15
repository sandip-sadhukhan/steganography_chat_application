from django.shortcuts import render, HttpResponse, redirect
from django.http import JsonResponse
from django.contrib.auth import login as auth_login, logout as auth_logout, authenticate
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import ImageStore
from stegano import lsb
from .utils import get_random_text


def home(request):
    return render(request, "pages/home.html")


def login(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        if user is not None:
            auth_login(request, user)
            messages.add_message(request, messages.SUCCESS, "Logged in successfully.")
            return redirect("/dashboard")
        else:
            messages.add_message(request, messages.ERROR, "Credentials not correct.")
            return redirect("/login")
    return render(request, "pages/login.html")


def signup(request):
    if request.method == "POST":
        first_name = request.POST["first_name"]
        last_name = request.POST["last_name"]
        username = request.POST["username"]
        email = request.POST["email"]
        password = request.POST["password"]

        user = User.objects.create_user(
            first_name=first_name,
            last_name=last_name,
            username=username,
            email=email,
            password=password,
        )

        user = authenticate(request, username=username, password=password)
        if user is not None:
            auth_login(request, user)
            messages.add_message(request, messages.SUCCESS, "Signed up successfully.")
            return redirect("/dashboard")
        else:
            messages.add_message(request, messages.ERROR, "Credentials not correct.")
            return redirect("/signup")

    return render(request, "pages/signup.html")


def logout(request):
    auth_logout(request)
    return redirect("/login")


@login_required
def dashboard(request):
    users = User.objects.all()
    users = users.exclude(id=request.user.id)
    context = {"users": users}
    return render(request, "pages/dashboard.html", context)


@login_required
def chat(request, username):
    me = request.user
    opponent = User.objects.get(username=username)
    context = {"me": me, "opponent": opponent}
    return render(request, "pages/chat.html", context)


# Image store route
@login_required
def uploadImage(request):
    image = request.FILES.get("image")
    if image is None:
        return JsonResponse({"success": False, "error": "Image not found"})
    else:
        imageStore = ImageStore.objects.create(user=request.user, image=image)
        return JsonResponse({"success": True, "fileURL": imageStore.get_image_url()})


# Steganography Encrept
@login_required
def encryptImage(request):
    if request.method == "POST":
        image = request.FILES.get("image")
        text = request.POST.get("text")
        if image is None:
            return JsonResponse({"success": False, "error": "Image not found"})
        elif text is None or len(text) == 0:
            return JsonResponse({"success": False, "error": "Text not found"})
        else:
            secret = lsb.hide(image, text)
            imagePath = f"./media/stegno_temp/{get_random_text(6)}_{image.name}"
            secret.save(imagePath)
            return JsonResponse({"success": True, "fileURL": imagePath[1:]})
    else:
        return HttpResponse("<h1>Get request not allowed!</h1>")


# Steganography Decrypt
def decryptImage(request):
    if request.method == "POST":
        imageURL = request.POST.get("image")
        if imageURL is None:
            return JsonResponse({"success": False, "error": "Image not found"})
        else:
            secretText = lsb.reveal(f"./{imageURL}")
            return JsonResponse({"success": True, "secretText": secretText})
    else:
        return HttpResponse("<h1>Get request not allowed!</h1>")
