from django.db import models
from django.contrib.auth.models import User


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_pic = models.ImageField(
        upload_to='profile_pics', max_length=200, default='default.jpg')
    auctions_following = models.CharField(
        max_length=200, blank=True, null=True)

    def __str__(self):
        return self.user.username
