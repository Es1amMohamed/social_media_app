from django.contrib.auth import get_user_model
from django.db import models
from django.urls import reverse
from django.utils.text import slugify
import uuid
from datetime import datetime
from django.core.validators import FileExtensionValidator

# Create your models here

User = get_user_model()


class Profile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    id_user = models.IntegerField(default=1)
    last_name = models.CharField(max_length=100, blank=True)
    bio = models.TextField(blank=True)
    profile_image = models.ImageField(upload_to="profile_images", default="photo12.jpg")
    location = models.CharField(max_length=100, blank=True)
    slug = models.SlugField(blank=True, null=True)

    def __str__(self):
        return self.user.username

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.user.username)

        super(Profile, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("users:settings", kwargs={"slug": self.slug})
    def get_profile_url(self):
        return reverse("users:profile", kwargs={"slug": self.slug})


class Post(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    author = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name="author")
    body = models.TextField(blank=True, null=True)
    image = models.ImageField(upload_to="post_images", blank=True, null=True)
    video = models.FileField(
        upload_to="videos_uploaded",
        blank=True,
        null=True,
        validators=[
            FileExtensionValidator(
                allowed_extensions=["MOV", "avi", "mp4", "webm", "mkv"]
            )
        ],
    )
    like = models.IntegerField(blank=True, null=True, default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.author.user.username


class LikePost(models.Model):
    post_id = models.CharField(max_length=500)
    username = models.CharField(max_length=100)
    comment = models.TextField(max_length=1000, blank=True, null=True)

    def __str__(self):
        return self.username


class Followers(models.Model):
    follower = models.CharField(max_length=100)
    user = models.CharField(max_length=100)

    def __str__(self):
        return self.follower