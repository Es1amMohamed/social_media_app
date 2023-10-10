from . import views
from django.urls import include, path
from .views import *

app_name = "users"

urlpatterns = [
    path("", views.index, name="index"),
    path("signup", views.signup, name="signup"),
    path("profile/<slug:slug>", views.profile, name="profile"),
    path("login", views.login, name="login"),
    path("logout", views.logout, name="logout"),
    path("settings/<slug:slug>", views.settings, name="settings"),
    path("upload", views.upload, name="upload"),
    path("like", views.like, name="like"),
    path("follow", views.follow, name="follow"),
]
