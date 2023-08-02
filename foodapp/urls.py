from django.urls import path
from . import views

app_name = "foodapp"
urlpatterns = [
    path('',views.index,name="home"),
    path('home',views.home_view, name="home"),
    path('login/', views.login_view, name="login"),
    path('signup/', views.registration_view, name="signup"),
    path('add_restaurant/', views.AddRestaurant.as_view(), name="add_restaurant"),
    path('go_back/', views.go_back, name="go_back"),
    path('restaurant_list/', views.RestaurantListView.as_view(), name='restaurant_list'),
    path('update_restaurant/<int:pk>/', views.UpdateRestaurant.as_view(), name="update_restaurant"),
    path('menu_list/<int:id>/', views.menu_list, name='menu_list'),
    path('restaurant/<int:id>/', views.RestaurantDetailView.as_view(), name='restaurant_detail'),
    path('delete_restaurant/<int:pk>/', views.DeleteRestaurant.as_view(), name="delete_restaurant"),
    path('add_food/<int:restaurant_id>/', views.add_food, name="add_food"),
    # path('menu_list/<int:food_id>/delete/', views.delete_food, name='delete_food'),
    path('add_to_cart/<int:food_id>/', views.add_to_cart, name='add_to_cart'),
    path('cart/', views.view_cart, name='cart'),
    path('remove_from_cart/<int:food_id>/', views.remove_from_cart, name='remove_from_cart'),
]
