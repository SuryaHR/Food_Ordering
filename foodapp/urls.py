from django.urls import path
from . import views

app_name = "foodapp"
urlpatterns = [
    path('',views.index,name="home"),
    path('home',views.home_view, name="home"),
    path('login/', views.login_view, name="login"),
    path('signup/', views.registration_view, name="signup"),
    path('add_restaurant/', views.AddRestaurant.as_view(), name="add_restaurant"),
    path('restaurant_list/', views.RestaurantListView.as_view(), name='restaurant_list'),
    path('menu_list/<int:id>/', views.menu_list, name='menu_list'),
    path('restaurant/<int:pk>/', views.RestaurantDetailView.as_view(), name='restaurant_detail'),
    path('add_food/<int:restaurant_id>/', views.add_food, name="add_food"),
]
