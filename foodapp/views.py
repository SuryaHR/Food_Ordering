from django.shortcuts import render, redirect
from django.contrib.auth.views import LogoutView
from django.contrib import messages
from django.urls import reverse_lazy
from django.contrib.auth import authenticate, login
from .forms import LoginForm, RestaurantForm, RegistrationForm
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView
from .models import Restaurant, Food

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
            form.save()
            return redirect('foodapp:login')  # Redirect to the login page after successful registration
    else:
        form = RegistrationForm()

    return render(request, 'foodapp/signup.html', {'form': form})

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
        return super().form_valid(form)

class RestaurantListView(ListView):
    model = Restaurant
    template_name = 'restaurant_list.html'
    context_object_name = 'restaurants'

class RestaurantDetailView(DetailView):
    model = Restaurant
    template_name = 'restaurant_detail.html'
    context_object_name = 'restaurant'

def menu_list(request, pk):
    restaurant = Restaurant.objects.get(pk=pk)
    foods = Food.objects.filter(restaurant=restaurant)
    return render(request, 'foodapp/menu_list.html', {'restaurant': restaurant, 'foods': foods})
