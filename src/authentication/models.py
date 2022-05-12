from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    
    profile_photo = models.ImageField(verbose_name='photo de profil')

    @property
    def number_of_subscribers(self):
        return self.followed_by.all().count()

    class Meta:
        ordering = ["username"]

    def __str__(self):
        return f"{self.username}"
