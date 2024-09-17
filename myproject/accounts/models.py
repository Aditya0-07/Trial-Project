from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    country = models.CharField(max_length=100)
    state = models.CharField(max_length=100)

