from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    user_id = models.IntegerField(blank=True, null=True)
    first_name = models.CharField(unique=True, max_length=20, blank=True, null=True)
    last_name = models.CharField(unique=True, max_length=20, blank=True, null=True)
    password = models.CharField(max_length=50, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)

    def __str__(self):
        return str(self.username)






