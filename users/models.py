from django.contrib.auth import get_user_model
from django.db import models

# Create your models here

User = get_user_model()


class Profile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    id_user = models.IntegerField(default=1)
    bio = models.TextField(blank=True)
    profile_image = models.ImageField(upload_to="profile_images", default="photo12.jpg")
    location = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return self.user.username
