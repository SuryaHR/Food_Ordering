from django.urls import path
from . import views

app_name = "foodapp"
urlpatterns = [
    path('',views.index,name="home"),
    path('home',views.home_view, name="home"),
    path('login/', views.login, name="login"),
    path('signup/', views.register, name="signup"),
    path('logout/', views.logout, name="logout"),
    path('add_restaurant/', views.AddRestaurant.as_view(), name="add_restaurant"),
    path('restaurant_list/', views.restaurant_list, name='restaurant_list'),
    path('update_restaurant/<int:pk>/', views.UpdateRestaurant.as_view(), name="update_restaurant"),
    path('menu_list/<int:id>/', views.menu_list, name='menu_list'),
    path('restaurant/<int:id>/', views.RestaurantDetailView.as_view(), name='restaurant_detail'),
    path('delete_restaurant/<int:pk>/', views.delete_restaurant, name="delete_restaurant"),
    path('add_food/<int:restaurant_id>/', views.add_food, name="add_food"),
    path('add_to_cart/<int:food_id>/', views.add_to_cart, name='add_to_cart'),
    path('cart/', views.view_cart, name='cart'),
    path('remove_from_cart/<int:food_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('delete_food/<int:pk>/', views.delete_food, name="delete_food"),
    path('foods/<int:food_id>/', views.food_detail, name='food_detail'),
    # path('order_confirmation/<int:food_id>/', views.order_confirmation, name='order_confirmation'),
    # path('payment/<int:food_id>/', views.payment, name='payment'),
    # path('complete_order/<int:order_id>/', views.complete_order, name='complete_order'),
    path('orders/', views.orders, name='orders'),
    path('create-checkout-session/<int:food_id>/', views.create_checkout_session, name='create_checkout_session'),
    path('payment_success/', views.payment_success, name='payment_success'),
]

