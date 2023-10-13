import random
from django.shortcuts import redirect, render
from django.contrib.auth.models import User, auth
from django.contrib import messages
from .models import *
from django.contrib.auth.decorators import login_required
from itertools import chain


# Create your views here.
@login_required(login_url="/login")
def index(request):
    user = Profile.objects.get(user=request.user)
    posts = Post.objects.all()
    users = Profile.objects.all()
    user_following = Followers.objects.filter(user=request.user.username)
    user_following_list = []
    feed = []
    for users_follow in user_following:
        user_following_list.append(users_follow.follower)
        print(users_follow.follower)
    for usernames in user_following_list:
        print(usernames)
        user_posted = User.objects.filter(username=usernames)
        feed.append(user_posted)
    feed_list = list(chain(*feed))

    all_users = User.objects.all()
    user_following_all = []

    for user in user_following:
        user_list = User.objects.get(username=user)
        user_following_all.append(user_list)

    new_suggestions_list = [
        x for x in list(all_users) if (x not in list(user_following_all))
    ]
    current_user = User.objects.filter(username=request.user.username)
    final_suggestions_list = [
        x for x in list(new_suggestions_list) if (x not in list(current_user))
    ]
    random.shuffle(final_suggestions_list)

    username_profile = []
    username_profile_list = []

    for users in final_suggestions_list:
        username_profile.append(users.id)

    for ids in username_profile:
        profile_lists = Profile.objects.filter(id_user=ids)
        username_profile_list.append(profile_lists)

    suggestions_username_profile_list = list(chain(*username_profile_list))

    context = {
        "user": user,
        "posts": posts,
        "users": users,
        "feed": feed_list,
        "suggestions_username_profile_list": suggestions_username_profile_list[:4],
    }
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
    follower = User.objects.get(username=request.user.username)
    user = User.objects.get(username=slug)
    profile = Profile.objects.get(user=user)
    posts = Post.objects.filter(author=profile)
    length = len(posts)
    if Followers.objects.filter(follower=user, user=follower).first():
        is_following = "Unfollow"
    else:
        is_following = "follow"
    user_following = len(Followers.objects.filter(user=slug))
    user_followers = len(Followers.objects.filter(follower=slug))
    context = {
        "follower": follower,
        "user": user,
        "profile": profile,
        "posts": posts,
        "length": length,
        "is_following": is_following,
        "user_following": user_following,
        "user_followers": user_followers,
    }

    return render(request, "users/profile.html", context)


def login(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user_confirm = User.objects.filter(username=username).exists()
        if user_confirm == True:
            user = auth.authenticate(username=username, password=password)
            if user is not None:
                auth.login(request, user)
                return redirect("/")
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
        follower = request.POST["follower"]
        user = request.POST["user"]
        if Followers.objects.filter(follower=follower, user=user).exists():
            delete_follow = Followers.objects.get(follower=follower, user=user)
            delete_follow.delete()
            return redirect("/profile/" + follower)
        else:
            new_follow = Followers.objects.create(follower=follower, user=user)
            new_follow.save()
            return redirect("/profile/" + follower)

    return render(request, "users/profile.html")


def search(request):
    user_profile = Profile.objects.get(user=request.user)
    if request.method == "POST":
        search_name = request.POST["search_name"]
        search_result = User.objects.filter(username__icontains=search_name)
        username_list = []
        username_profile_list = []
        for users in search_result:
            username_list.append(users.id)
        for id in username_list:
            profile = Profile.objects.filter(id_user=id)
            username_profile_list.append(profile)
        username_profile_list = list(chain(*username_profile_list))
        return render(
            request,
            "users/search.html",
            {
                "user_profile": user_profile,
                "username_profile_list": username_profile_list,
                "search_name": search_name,
            },
        )
    no_result = "No result found"
    return render(
        request,
        "users/search.html",
        {"user_profile": user_profile, "no_result": no_result},
    )
