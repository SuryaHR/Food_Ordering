from django.contrib import admin
from .models import CustomUser, Restaurant,Food
# Register your models here.

admin.site.register(CustomUser)
admin.site.register(Restaurant)
admin.site.register(Food)
