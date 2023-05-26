from django.contrib.auth.models import AbstractUser
from django.db import models

from .managers import CustomUserManager


class CustomUser(AbstractUser):
    username = None  # by default username for auth
    email = models.EmailField('email address', unique=True)

    USERNAME_FIELD = 'email'  # use email field as username
    REQUIRED_FIELDS = []  # for createsuperuser  #TODO:first_name, last_name

    objects = CustomUserManager()

    def __str__(self):
        return self.email
