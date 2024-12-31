from django.shortcuts import render
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.hashers import make_password
from django.contrib import messages
from .models import *
from django.contrib.auth import get_user_model

# Use the get_user_model function to get the custom user model
User = get_user_model()

# Create your views here.
def home(request):
    return render (request, "home.html")


# Admin Dashboard
def admin_dashboard(request):
    return render(request, 'admin/admin_dashboard.html')

# Supplier Dashboard
def supplier_dashboard(request):
    return render(request, 'supplier/supplier_dashboard.html')

# User Dashboard
def user_dashboard(request):
    return render(request, 'user/user_dashboard.html')


# Register Supplier
def register_supplier(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        company_name = request.POST.get('company_name')
        contact_info = request.POST.get('contact_info')

        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username already exists.')
            return redirect('register_supplier')

        supplier_user = User.objects.create(
            username=username,
            email=email,
            password=make_password(password),
            role='supplier',
        )
        Supplier.objects.create(user=supplier_user, company_name=company_name, contact_info=contact_info)
        messages.success(request, 'Supplier registered successfully!')
        return redirect('login')

    return render(request, 'supplier/register_supplier.html')

# Register User
def register_user(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')

        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username already exists.')
            return redirect('register_user')

        User.objects.create(
            username=username,
            email=email,
            password=make_password(password),
            role='user',
        )
        messages.success(request, 'User registered successfully!')
        return redirect('login')

    return render(request, 'user/register_user.html')

# Login for All Roles
def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        # Authenticate the user using the custom User model
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            messages.success(request, 'Login successful!')

            # Debugging output to check if user and role are correct
            print(f"User: {user}, Role: {user.role}")

            # Redirect based on the user's role
            if user.is_superuser:
                return redirect('/admin_dashboard/')
            elif user.role == 'supplier':
                return redirect('/supplier_dashboard/')
            elif user.role == 'user':
                return redirect('/user_dashboard/')
            else:
                messages.error(request, 'Invalid role assigned to the user.')
                return redirect('login')
        else:
            # If authentication fails, show an error message
            messages.error(request, 'Invalid username or password.')
            return redirect('login')

    return render(request, 'login.html')
