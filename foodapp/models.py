from django.db import models

from django.contrib.auth.models import AbstractUser
# Create your models here.

class CustomUser(AbstractUser):
    # Add any additional fields you want to store for the user
    # For example, email, contact, etc.
    email = models.EmailField(unique=True)
    contact = models.CharField(max_length=15)

class Restaurant(models.Model):
    restaurant_name = models.CharField(max_length=30)
    restaurant_image = models.ImageField(upload_to='media', default='')

    def __str__(self):
        return self.restaurant_name

class Food(models.Model):
    food_name = models.CharField(max_length=30)
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE)
    food_image = models.ImageField(upload_to='media', default='')

    def __str__(self):
        return self.food_name