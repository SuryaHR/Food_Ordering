from django.conf import settings
from django.http import JsonResponse
import stripe
from django.shortcuts import render, redirect,get_object_or_404
from django.contrib import messages
from django.contrib.auth import authenticate, login
from .forms import RestaurantForm,FoodForm
from django.urls import reverse_lazy, reverse
from django.views.generic import DetailView, CreateView,UpdateView
from .models import Restaurant,Food,CartItem, CustomUser, Order
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

stripe.api_key = settings.STRIPE_SECRET_KEY

# Create your views here.

def index(request):
    # If the user is logged in, redirect to the restaurant_list page
    if request.user.is_authenticated:
        return redirect('foodapp:restaurant_list')
    
    return render(request, 'foodapp/index.html')

def home_view(request):
    return render(request, 'foodapp/index.html')

def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        try:
            user = CustomUser.objects.get(username=username)
            print("User Role:", user.role) 
            if user.password == password:
                request.session['is_login'] = True
                request.session['user_role'] = user.role  
                request.session['user_id'] = user.id
                print("Session Variable is_login:", request.session.get('is_login'))
                # Successful login
                print("User Role:", user.role)
                return redirect('foodapp:restaurant_list')
            else:
                error_msg = "Invalid password."
                return render(request, 'foodapp/login.html', {'error_msg': error_msg})
        except CustomUser.DoesNotExist:
            error_msg = "Invalid username."
            return render(request, 'foodapp/login.html', {'error_msg': error_msg})
    
    return render(request, 'foodapp/login.html')

def register(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        contact = request.POST['contact']
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']
        role = request.POST['role']

        if password == confirm_password and len(password) >= 6:
            user = CustomUser.objects.create(
                username=username, 
                password=password,
                email=email,
                contact=contact,
                role=role,
            )
            request.session['user_id'] = user.id  # Store the user's ID in the session
            return redirect('foodapp:login')
        else:
            error_msg = "Passwords do not match or are too short."
            return render(request, 'foodapp/signup.html', {'error_msg': error_msg})
   
    return render(request, 'foodapp/signup.html')

def logout(request):
    request.session['is_login'] = False
    return redirect('foodapp:login')

class AddRestaurant(CreateView):
    model = Restaurant
    form_class = RestaurantForm
    template_name = 'foodapp/restaurant_form.html'
    success_url = reverse_lazy('foodapp:restaurant_list')

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
    
def restaurant_list(request):
    restaurants = Restaurant.objects.all()
    user = request.user  # Assuming you have the user object in your request
    # print("User Role in View:", user.role)
    context = {
        'restaurants': restaurants,
        'user': user,
    }
    return render(request, 'foodapp/restaurant_list.html', context)

class RestaurantDetailView(DetailView):
    model = Restaurant
    template_name = 'restaurant_detail.html'
    context_object_name = 'restaurant'

class UpdateRestaurant(UpdateView):
    model = Restaurant
    fields = '__all__'
    template_name = 'foodapp/restaurant_form.html'
    success_url = reverse_lazy('foodapp:restaurant_list')

def delete_restaurant(request, pk):
    restaurant = get_object_or_404(Restaurant, pk=pk)
    if request.method == 'POST':
        restaurant.delete()
    return redirect(request.POST.get('next', 'foodapp:restaurant_list'))

def menu_list(request, id):
    restaurant = get_object_or_404(Restaurant, id=id)
    foods = Food.objects.filter(restaurant=restaurant)
    return render(request, 'foodapp/menu_list.html', {
        'restaurant': restaurant,
        'foods': foods,
        'STRIPE_PUBLISHABLE_KEY': settings.STRIPE_PUBLISHABLE_KEY,
    })

def food_detail(request, food_id):
    food = get_object_or_404(Food, pk=food_id)
    return render(request, 'foodapp/food_detail.html', {'food': food})

def delete_food(request, pk):
    food = get_object_or_404(Food, pk=pk)
    if request.method == 'POST':
        restaurant_id = food.restaurant.id  # Get the restaurant's ID
        food.delete()
        return redirect(reverse('foodapp:menu_list', kwargs={'id': restaurant_id}))
    
    return redirect(request.POST.get('next', 'foodapp:menu_list'))

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

def add_to_cart(request, food_id):
    food = get_object_or_404(Food, pk=food_id)
    user_id = request.session.get('user_id')  # Get user ID from the session
    if user_id is None:
        return redirect('foodapp:login')  # Redirect to login if user is not logged in

    user = get_object_or_404(CustomUser, pk=user_id)
    cart_item, created = CartItem.objects.get_or_create(food=food, user=user)
    if not created:
        cart_item.quantity += 1
        cart_item.save()
    messages.success(request, f"{food.food_name} added to the cart!")

    return redirect('foodapp:restaurant_list')

def view_cart(request):
    user_id = request.session.get('user_id')  # Get user ID from the session
    if user_id is None:
        return redirect('foodapp:login')  # Redirect to login if user is not logged in

    user = get_object_or_404(CustomUser, pk=user_id)
    cart_items = CartItem.objects.filter(user=user)
    return render(request, 'foodapp/cart.html', {'cart_items': cart_items})

def remove_from_cart(request, food_id):
    food = get_object_or_404(Food, pk=food_id)
    user_id = request.session.get('user_id')  # Get user ID from the session
    if user_id is None:
        return redirect('foodapp:login')  # Redirect to login if user is not logged in

    user = get_object_or_404(CustomUser, pk=user_id)

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

def orders(request):
    if request.session.is_login: 
        if request.session.user_role == 'admin':
            # Fetch all orders for admins
            orders = Order.objects.all()
        else:
            # Fetch orders for the current user
            orders = Order.objects.filter(user=request.user)
    else:
        # Redirect non-logged in users to login page
        return redirect('foodapp:login')

    return render(request, 'foodapp/orders.html', {'orders': orders})

def payment_success(request):
    return render(request, 'foodapp/payment_success.html')

def create_checkout_session(request, food_id):
    food = get_object_or_404(Food, pk=food_id)
    session = stripe.checkout.Session.create(
        payment_method_types=['card'],
        line_items=[
            {
                'price_data': {
                    'currency': 'inr',  # Change this to the appropriate currency
                    'unit_amount_decimal': int(food.price * 100),  # Convert to cents
                    'product_data': {
                        'name': food.food_name,
                    },
                },
                'quantity': 1,
            },
        ],
        mode='payment',
        success_url=request.build_absolute_uri(reverse('foodapp:payment_success')),
        cancel_url=request.build_absolute_uri(reverse('foodapp:cart')),
    )
    return JsonResponse({'sessionId': session.id})