from django.db import models
# Create your models here.

class CustomUser(models.Model):
    username = models.CharField(max_length=100)
    password = models.CharField(max_length=100)
    email = models.EmailField(max_length=100, default='', unique=True)
    contact = models.CharField(max_length=20, default='')
    is_login = models.BooleanField(default=False)
    ROLE_CHOICES = (
        ('admin', 'Admin'),
        ('user', 'User'),
    )

    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='user')

    # Add more fields as needed

    def __str__(self):
        return self.username

class Restaurant(models.Model):
    id = models.AutoField(primary_key=True)
    restaurant_name = models.CharField(max_length=30)
    restaurant_image = models.ImageField(upload_to='media', default='')

    def __str__(self):
        return self.restaurant_name

class Food(models.Model):
    food_name = models.CharField(max_length=30)
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE)
    food_image = models.ImageField(upload_to='media', default='')
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    def __str__(self):
        return self.food_name
    
class CartItem(models.Model):
    food = models.ForeignKey(Food, on_delete=models.CASCADE)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, default=1)
    quantity = models.PositiveIntegerField(default=1)

class Order(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    food = models.ForeignKey(Food, on_delete=models.CASCADE)
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE) 
    ordered_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Order {self.id} - {self.user.username} - {self.food.food_name}"

