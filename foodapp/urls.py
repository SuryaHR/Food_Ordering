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
    path('menu_list/<int:id>/', views.menu_list, name='menu_list'),
    path('restaurant/<int:id>/', views.RestaurantDetailView.as_view(), name='restaurant_detail'),
    path('add_food/<int:restaurant_id>/', views.add_food, name="add_food"),
    path('add_to_cart/<int:food_pk>/', views.add_to_cart, name='add_to_cart'),
    path('cart/', views.view_cart, name='cart'),
    path('place_order/<int:food_pk>/', views.place_order, name='place_order'),
]
