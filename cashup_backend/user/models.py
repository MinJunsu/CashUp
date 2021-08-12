from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.
class User(AbstractUser):
    api_key = models.CharField(max_length=30)
    api_secret_key = models.CharField(max_length=30)