from django.shortcuts import render, redirect
from django.contrib.auth.views import LogoutView
from django.contrib import messages
from django.urls import reverse_lazy
#from .models import Food, Restaurant
from django.views.generic import CreateView, ListView
from django.contrib.auth import authenticate, login
from .forms import LoginForm

from django.urls import reverse_lazy
from .forms import RegistrationForm

# Create your views here.
def index(request):
    return render(request,'foodapp/index.html')

def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('foodapp:home')  # Redirect to the home page after successful login
            else:
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

