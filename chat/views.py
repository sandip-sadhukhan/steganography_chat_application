from django.shortcuts import render, HttpResponse

def home(request):
    return render(request, 'pages/home.html')