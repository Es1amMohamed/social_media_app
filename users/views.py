from django.shortcuts import redirect, render
from django.contrib.auth.models import User, auth
from django.contrib import messages
from .models import *
from django.contrib.auth.decorators import login_required


# Create your views here.
@login_required(login_url="/login")
def index(request):
    user = Profile.objects.get(user=request.user)
    posts = Post.objects.all()
    context = {"user": user, "posts": posts}
    return render(request, "users/index.html", context)


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
                return redirect("/")
        else:
            messages.info(request, "Password Not Matching")
            return redirect("/signup")
    else:
        return render(request, "users/signup.html")


@login_required(login_url="/login")
def profile(request, slug):
    user = User.objects.get(username=slug)
    profile = Profile.objects.get(user=user)
    posts = Post.objects.filter(user=user)
    length = len(posts)
    context = {"user": user, "profile": profile, "posts": posts, "length": length}
    
    return render(request, "users/profile.html" , context)


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
def settings(request, slug):
    user = Profile.objects.get(user=request.user)
    if request.method == "POST":
        if request.FILES.get("image") == None:
            image = user.profile_image
            user.user.username = request.POST["firstname"]
            user.last_name = request.POST["lastname"]
            user.user.email = request.POST["email"]
            user.bio = request.POST["bio"]
            user.location = request.POST["location"]
            user.profile_image = image
            user.save()
            return redirect("/")
        if request.FILES.get("image") != None:
            image = request.FILES.get("image")
            user.user.username = request.POST["firstname"]
            user.last_name = request.POST["lastname"]
            user.user.email = request.POST["email"]
            user.bio = request.POST["bio"]
            user.location = request.POST["location"]
            user.profile_image = image
            user.save()
            return redirect("/")

    else:
        return render(request, "users/setting.html", {"user": user})


@login_required(login_url="/login")
def upload(request):
    if request.method == "POST":
        user = request.user
        body = request.POST["body"]
        image = request.FILES.get("image")
        video = request.FILES.get("video")
        new_post = Post.objects.create(user=user, body=body, image=image, video=video)
        new_post.save()
        return redirect("/")
    else:
        return render(request, "/")


@login_required(login_url="/login")
def like(request):
    username = request.user.username
    post_id = request.GET.get("post_id")
    comment = request.GET.get("comment")
    post = Post.objects.get(id=post_id)
    like_filter = LikePost.objects.filter(post_id=post_id, username=username).first()
    if like_filter == None:
        new_like = LikePost.objects.create(
            post_id=post_id, username=username, comment=comment
        )
        new_like.save()
        post.like = post.like + 1
        post.save()
        return redirect("/")
    else:
        like_filter.delete()
        post.like -= 1
        post.save()
        return redirect("/")

@login_required(login_url="/login")
def follow(request):
    if request.method == "POST":
        follower = request.POST['follower']
        user = request.POST["user"]
        if Followers.objects.filter(follower=follower, user=user).exists():
            delete_follow = Followers.objects.get(follower=follower, user=user)
            delete_follow.delete()
            return redirect("/profile/"+user)
        else:
            new_follow = Followers.objects.create(follower=follower, user=user)
            new_follow.save()
            return redirect("/profile/"+user)
    else:
        return render(request, "users/profile.html")