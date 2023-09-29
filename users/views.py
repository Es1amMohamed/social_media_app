from django.shortcuts import redirect, render
from django.contrib.auth.models import User, auth
from django.contrib import messages
from .models import *
from django.contrib.auth.decorators import login_required


# Create your views here.
@login_required(login_url="/login")
def index(request):
    return render(request, "users/index.html")


def signup(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        password2 = request.POST["password2"]
        email = request.POST["email"]

        if password == password2:
            if User.objects.filter(email=email).exists():
                messages.info(request, "Email Exists")
                return redirect("/signup")
            elif User.objects.filter(username=username).exists():
                messages.info(request, "Username Exists")
                return redirect("/signup")
            else:
                user = User.objects.create_user(
                    username=username, password=password, email=email
                )
                user.save()
                user_login = auth.authenticate(username=username, password=password)
                auth.login(request, user_login)
                user_model = User.objects.get(username=username)
                profile = Profile.objects.create(user=user_model, id_user=user_model.id)
                profile.save()
                return redirect("/settings")
        else:
            messages.info(request, "Password Not Matching")
            return redirect("/signup")
    else:
        return render(request, "users/signup.html")


@login_required(login_url="/login")
def profile(request):
    return render(request, "users/profile.html")


def login(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user_confirm = User.objects.filter(username=username).exists()
        if user_confirm == True:
            user = auth.authenticate(username=username, password=password)
            if user is not None:
                auth.login(request, user)
                return redirect("/profile")
            else:
                messages.info(request, "Wrong Password")
                return redirect("/login")
        else:
            messages.info(request, "Username does not exist ")
            return redirect("/signup")
    else:
        return render(request, "users/login.html")


def logout(request):
    auth.logout(request)
    return redirect("/login")


@login_required(login_url="/login")
def settings(request):
    return render(request, "users/setting.html")
