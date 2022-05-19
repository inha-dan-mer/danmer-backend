from django.db import models
from django.contrib.auth.models import AbstractUser, UserManager



class User(AbstractUser):
    objects = UserManager()
    
    class Meta(AbstractUser.Meta):
        swappable = "AUTH_USER_MODEL"

    def __str__(self):
        return self.username