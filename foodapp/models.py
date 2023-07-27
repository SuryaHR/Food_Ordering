from django.db import models

from django.contrib.auth.models import AbstractUser
# Create your models here.

class CustomUser(AbstractUser):
    # Add any additional fields you want to store for the user
    # For example, email, contact, etc.
    email = models.EmailField(unique=True)
    contact = models.CharField(max_length=15)
