from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("login/", views.login, name="login"),
    path("signup/", views.signup, name="signup"),
    path("logout/", views.logout, name="logout"),
    path("dashboard/", views.dashboard, name="dashboard"),
    path("chat/<str:username>/", views.chat, name="chat"),
    path("upload-image/", views.uploadImage, name="uploadImage"),
]
