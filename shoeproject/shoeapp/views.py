from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login
from django.contrib.auth.hashers import make_password
from django.contrib import messages
from .models import *
from django.http import Http404
from django.contrib.auth import get_user_model

# Use the get_user_model function to get the custom user model
User = get_user_model()

# Create your views here.
def home(request):
    return render (request, "home.html")

# Admin Dashboard
def admin_dashboard(request):
    return render(request, 'admin/admin_dashboard.html')


def approve_user(request, user_id):
    # Ensure that the logged-in user is an admin
    if not request.user.is_superuser:
        raise Http404("You are not authorized to approve users.")
    
    user = get_object_or_404(User, id=user_id)

    # Check if the user is already approved
    if user.is_approved:
        messages.info(request, f"User {user.username} is already approved.")
    else:
        # Approve the user
        user.is_approved = True
        user.save()
        messages.success(request, f"User {user.username} has been approved.")
    
    return redirect('admin_dashboard')

def approve_supplier(request, supplier_id):
    # Ensure that the logged-in user is an admin
    if not request.user.is_superuser:
        raise Http404("You are not authorized to approve suppliers.")
    
    supplier = get_object_or_404(Supplier, id=supplier_id)
    
    # Check if the supplier is already approved
    if supplier.user.is_approved:
        messages.info(request, f"Supplier {supplier.company_name} is already approved.")
    else:
        # Approve the supplier
        supplier.user.is_approved = True
        supplier.user.save()
        messages.success(request, f"Supplier {supplier.company_name} has been approved.")
    
    return redirect('admin_dashboard')

def view_all_users(request):
    # Fetch all users who are not superusers and whose role is not 'supplier'
    users = User.objects.filter(is_superuser=False).exclude(role='supplier')
    
    # Render the template and pass the filtered list of users
    return render(request, 'admin/view_all_users.html', {'users': users})


def view_all_suppliers(request):
    # Fetch all suppliers
    suppliers = Supplier.objects.all()
    
    # Render the template and pass the list of suppliers
    return render(request, 'admin/view_all_suppliers.html', {'suppliers': suppliers})

def update_user(request, user_id):
    user = get_object_or_404(User, id=user_id)

    if request.method == 'POST':
        new_username = request.POST.get('username')
        new_email = request.POST.get('email')
        new_role = request.POST.get('role')

        # Validate the inputs (basic validation for example)
        if new_username and new_email and new_role in ['admin', 'supplier', 'user']:
            user.username = new_username
            user.email = new_email
            user.role = new_role
            user.save()
            messages.success(request, f'User {user.username} updated successfully.')
        else:
            messages.error(request, 'Invalid input.')

        return redirect('view_all_users')  # Redirect to the page showing all users

    return render(request, 'admin/update_user.html', {'user': user})

def update_supplier(request, supplier_id):
    supplier = get_object_or_404(Supplier, id=supplier_id)

    if request.method == 'POST':
        new_company_name = request.POST.get('company_name')
        new_contact_info = request.POST.get('contact_info')

        if new_company_name:
            supplier.company_name = new_company_name
        if new_contact_info:
            supplier.contact_info = new_contact_info

        supplier.save()
        messages.success(request, f'Supplier {supplier.company_name} updated successfully.')

        return redirect('view_all_suppliers')  # Redirect to the page showing all suppliers

    return render(request, 'admin/update_supplier.html', {'supplier': supplier})


def delete_user(request, user_id):
    user = get_object_or_404(User, id=user_id)

    if request.method == 'POST':  # Ensure deletion is a POST request
        user.delete()
        messages.success(request, f'User {user.username} deleted successfully.')
        return redirect('view_all_users')  # Redirect to the page showing all users

    return render(request, 'admin/delete_user.html', {'user': user})

def delete_supplier(request, supplier_id):
    supplier = get_object_or_404(Supplier, id=supplier_id)

    if request.method == 'POST':  # Ensure deletion is a POST request
        supplier.delete()
        messages.success(request, f'Supplier {supplier.company_name} deleted successfully.')
        return redirect('view_all_suppliers')  # Redirect to the page showing all suppliers

    return render(request, 'admin/delete_supplier.html', {'supplier': supplier})

#______________________________________________________________________________________________________________#

# Supplier Dashboard
def supplier_dashboard(request):
    return render(request, 'supplier/supplier_dashboard.html')

def add_category(request):
    if request.method == 'POST':
        category_name = request.POST.get('category_name')
        category_description = request.POST.get('category_description', '')

        if category_name:
            try:
                # Get the supplier associated with the logged-in user
                supplier = request.user.supplier  

                # Create the new category for the logged-in supplier
                ProductCategory.objects.create(
                    name=category_name,
                    description=category_description,
                    supplier=supplier
                )
                messages.success(request, 'Category added successfully!')
                return redirect('view_all_categories')  # Redirect to the page displaying all categories
            except Supplier.DoesNotExist:
                # Handle the case where the user is not associated with a supplier
                messages.error(request, 'You must be a supplier to add categories.')
                return redirect('supplier_dashboard')  # Redirect to the supplier dashboard or another appropriate page
        else:
            messages.error(request, 'Category name is required!')

    return render(request, 'supplier/add_category.html')

# Update Category for Supplier
def update_category(request, category_id):
    category = get_object_or_404(ProductCategory, id=category_id)
    if request.method == 'POST':
        category.name = request.POST.get('category_name', category.name)
        category.description = request.POST.get('category_description', category.description)
        category.save()
        messages.success(request, 'Category updated successfully!')
        return redirect('view_all_categories')  # Redirect to the page displaying all categories
    return render(request, 'supplier/update_category.html', {'category': category})

# Delete Category for Supplier
def delete_category(request, category_id):
    category = get_object_or_404(ProductCategory, id=category_id)
    category.delete()
    messages.success(request, 'Category deleted successfully!')
    return redirect('view_all_categories')  # Redirect to the page displaying all categories

# Add Product for Supplier
def add_product(request):
    if request.method == 'POST':
        product_name = request.POST.get('product_name')
        product_category_id = request.POST.get('category')
        product_description = request.POST.get('description', '')
        product_price = request.POST.get('price')
        product_stock = request.POST.get('stock')
        supplier = request.user.supplier  # Get the supplier from the logged-in user
        
        if product_name and product_price and product_stock:
            category = get_object_or_404(ProductCategory, id=product_category_id)
            Product.objects.create(
                name=product_name,
                category=category,
                description=product_description,
                price=product_price,
                stock=product_stock,
                supplier=supplier
            )
            messages.success(request, 'Product added successfully!')
            return redirect('view_all_products')  # Redirect to the page displaying all products
        else:
            messages.error(request, 'Product name, price, and stock are required!')
    categories = ProductCategory.objects.all()
    return render(request, 'supplier/add_product.html', {'categories': categories})

# Update Product for Supplier
def update_product(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    if request.method == 'POST':
        product.name = request.POST.get('product_name', product.name)
        product.category = get_object_or_404(ProductCategory, id=request.POST.get('category', product.category.id))
        product.description = request.POST.get('description', product.description)
        product.price = request.POST.get('price', product.price)
        product.stock = request.POST.get('stock', product.stock)
        product.save()
        messages.success(request, 'Product updated successfully!')
        return redirect('view_all_products')  # Redirect to the page displaying all products
    categories = ProductCategory.objects.all()
    return render(request, 'supplier/update_product.html', {'product': product, 'categories': categories})

# Delete Product for Supplier
def delete_product(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    product.delete()
    messages.success(request, 'Product deleted successfully!')
    return redirect('view_all_products')  # Redirect to the page displaying all products

def view_all_categories(request):
    # Filter categories by the logged-in supplier
    supplier = request.user.supplier
    categories = ProductCategory.objects.filter(supplier=supplier)
    return render(request, 'supplier/view_all_categories.html', {'categories': categories})

# View all products added by the supplier
def view_all_products(request):
    # Filter products by the logged-in supplier
    supplier = request.user.supplier
    products = Product.objects.filter(supplier=supplier)
    return render(request, 'supplier/view_all_products.html', {'products': products})


#______________________________________________________________________________________________________________#

# User Dashboard
def user_dashboard(request):
    return render(request, 'user/user_dashboard.html')

#______________________________________________________________________________________________________________#
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
            if user.is_superuser:
                    return redirect('/admin_dashboard/')
            # Check if the user is approved
            elif user.is_approved:
                login(request, user)
                messages.success(request, 'Login successful!')

                # Debugging output to check if user and role are correct
                print(f"User: {user}, Role: {user.role}")

                # Redirect based on the user's role
                if user.role == 'supplier':
                    return redirect('/supplier_dashboard/')
                elif user.role == 'user':
                    return redirect('/user_dashboard/')
                else:
                    messages.error(request, 'Invalid role assigned to the user.')
                    return redirect('login')
            else:
                messages.error(request, 'Your account is not approved yet. Please contact the admin.')
                return redirect('login')
        else:
            # If authentication fails, show an error message
            messages.error(request, 'Invalid username or password.')
            return redirect('login')

    return render(request, 'login.html')

