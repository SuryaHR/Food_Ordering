from django.shortcuts import render, redirect,get_object_or_404
from django.contrib.auth.views import LogoutView
from django.contrib import messages
from django.urls import reverse_lazy
from django.contrib.auth import authenticate, login
from .forms import LoginForm, RestaurantForm, RegistrationForm,FoodForm
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView
from .models import Restaurant,Food,CartItem,Order

# Create your views here.

def index(request):
    # If the user is logged in, redirect to the restaurant_list page
    if request.user.is_authenticated:
        return redirect('foodapp:restaurant_list')
    
    return render(request, 'foodapp/index.html')

def home_view(request):
    return render(request, 'foodapp/index.html')

def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']

            print("Received username:", username)
            print("Received password:", password)

            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                print("Login successful!")
                return redirect('foodapp:restaurant_list')  # Redirect to the home page after successful login
            else:
                print("Login failed. Invalid username or password.")
                messages.error(request, 'Invalid username or password. Please try again.')
    else:
        form = LoginForm()

    return render(request, 'foodapp/login.html', {'form': form})

def registration_view(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            print("Form data is valid:")
            print(form.cleaned_data)
            user = form.save(commit=False)
            role = form.cleaned_data.get('role')
            if role == 'admin':
                user.is_staff = True
            user.save()
            print("User registered successfully.")
            return redirect('foodapp:login')  # Redirect to the login page after successful registration
        else:
            print("Form data is invalid:")
            print(form.errors)
    else:
        form = RegistrationForm()

    return render(request, 'foodapp/signup.html', {'form': form})

def go_back(request):
    previous_page = request.META.get('HTTP_REFERER')
    return redirect(previous_page)

class AddRestaurant(CreateView):
    model = Restaurant
    form_class = RestaurantForm
    template_name = 'foodapp/restaurant_form.html'
    success_url = reverse_lazy("foodapp:restaurant_list")

    def form_valid(self, form):
        # This method is called when the form is valid.
        # Print the form data in the terminal.
        print("Received restaurant name:", form.cleaned_data['restaurant_name'])
        print("Received restaurant image:", form.cleaned_data['restaurant_image'])
        restaurant_name = form.cleaned_data['restaurant_name']
        if Restaurant.objects.filter(restaurant_name=restaurant_name).exists():
            messages.error(self.request, f"A restaurant with the name '{restaurant_name}' already exists.")
            return redirect('foodapp:add_restaurant')
        return super().form_valid(form)

class RestaurantListView(ListView):
    model = Restaurant
    template_name = 'restaurant_list.html'
    context_object_name = 'restaurants'

class RestaurantDetailView(DetailView):
    model = Restaurant
    template_name = 'restaurant_detail.html'
    context_object_name = 'restaurant'

def menu_list(request, id):
    restaurant = get_object_or_404(Restaurant, id=id)
    foods = Food.objects.filter(restaurant=restaurant)
    return render(request, 'foodapp/menu_list.html', {'restaurant': restaurant, 'foods': foods})

def add_food(request, restaurant_id):
    restaurant = Restaurant.objects.get(id=restaurant_id)

    if request.method == 'POST':
        form = FoodForm(request.POST, request.FILES)
        if form.is_valid():
            food = form.save(commit=False)
            food.restaurant = restaurant
            food.save()
            return redirect('foodapp:menu_list', id=restaurant_id)
    else:
        form = FoodForm()

    return render(request, 'foodapp/add_food.html', {'form': form, 'restaurant': restaurant})

# def delete_food(request, food_id):
#     if not request.user.is_staff:
#         return redirect('foodapp:menu_list')

#     food = get_object_or_404(Food, pk=food_id)

#     if request.method == 'POST':
#         # Delete the food item
#         food.delete()
#         messages.success(request, f"{food.food_name} deleted successfully.")
#         return redirect('foodapp:menu_list')

#     context = {
#         'foods': Food.objects.all(),
#     }

#     return render(request, 'foodapp/menu_list.html', context)

def add_to_cart(request, food_id):
    food = get_object_or_404(Food, pk=food_id)
    user = request.user
    cart_item, created = CartItem.objects.get_or_create(food=food, user=user)
    if not created:
        cart_item.quantity += 1
        cart_item.save()
    messages.success(request, f"{food.food_name} added to the cart!")

    return redirect('foodapp:restaurant_list')

def view_cart(request):
    user = request.user
    cart_items = CartItem.objects.filter(user=user)
    return render(request, 'foodapp/cart.html', {'cart_items': cart_items})

def remove_from_cart(request, food_id):
    food = get_object_or_404(Food, pk=food_id)
    user = request.user

    try:
        cart_item = CartItem.objects.get(food=food, user=user)

        # If the quantity is greater than 1, decrease it by 1
        if cart_item.quantity > 1:
            cart_item.quantity -= 1
            cart_item.save()
            messages.success(request, f"One quantity of {food.food_name} removed from the cart.")
        else:
            cart_item.delete()
            messages.success(request, f"{food.food_name} removed from the cart.")
    except CartItem.DoesNotExist:
        messages.error(request, "Item not found in the cart.")

    return redirect('foodapp:cart')


def place_order(request, food_pk):
    food = Food.objects.get(pk=food_pk)
    order, created = Order.objects.get_or_create(user=request.user, food=food)
    if not created:
        order.quantity += 1
        order.save()
    return redirect('foodapp:menu_list', restaurant_pk=food.restaurant.pk)
