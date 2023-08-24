from django import forms
from foodapp.models import Restaurant,Food

class RestaurantForm(forms.ModelForm):
    class Meta:
        model = Restaurant
        fields = ['restaurant_name', 'restaurant_image']

class FoodForm(forms.ModelForm):
    class Meta:
        model = Food
        fields = ['food_name', 'food_image','price']
