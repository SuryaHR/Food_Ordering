from django.urls import path
from . import views

app_name = "foodapp"
urlpatterns = [
    path('',views.index,name="home"),
    path('login/', views.login_view, name="login"),
    path('signup/', views.registration_view, name="signup"),
#    path('logout/', views.CustomLogoutView.as_view(), name="logout"),
#    path('add_restaurant/', views.AddRestaurant.as_view(),name="add_restaurant"),
#    path('restaurant_list/', views.RestaurantList.as_view(),name="restaurant_list"),
]
