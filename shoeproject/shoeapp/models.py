from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    ROLE_CHOICES = [
        ('admin', 'Admin'),
        ('supplier', 'Supplier'),
        ('user', 'User'),
    ]
    role = models.CharField(max_length=10, choices=ROLE_CHOICES)

    groups = models.ManyToManyField(
        'auth.Group',
        related_name='shoeapp_user_set',
        blank=True,
        help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.',
        verbose_name='groups',
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='shoeapp_user_permissions_set',
        blank=True,
        help_text='Specific permissions for this user.',
        verbose_name='user permissions',
    )


# Product Category Model
class ProductCategory(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    
    def __str__(self):
        return self.name

# Product Model
class Product(models.Model):
    name = models.CharField(max_length=200)
    category = models.ForeignKey(ProductCategory, on_delete=models.CASCADE, related_name="products")
    description = models.TextField(blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.PositiveIntegerField()
    supplier = models.ForeignKey('Supplier', on_delete=models.SET_NULL, null=True, blank=True, related_name="products")

    def __str__(self):
        return self.name

# Supplier Model
class Supplier(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="supplier")
    company_name = models.CharField(max_length=200)
    contact_info = models.TextField()

    def __str__(self):
        return self.company_name

# Order Model
class Order(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('shipped', 'Shipped'),
        ('delivered', 'Delivered'),
        ('canceled', 'Canceled'),
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="orders")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Order {self.id} - {self.status}"

# Order Item Model
class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="items")
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="order_items")
    quantity = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.product.name} (x{self.quantity})"

# Wishlist Model
class Wishlist(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="wishlist")
    products = models.ManyToManyField(Product, related_name="wishlisted_by")

    def __str__(self):
        return f"{self.user.username}'s Wishlist"

# Cart Model
class Cart(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="cart")
    products = models.ManyToManyField(Product, through='CartItem', related_name="in_carts")

    def __str__(self):
        return f"{self.user.username}'s Cart"

# Cart Item Model
class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name="cart_items")
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="cart_items")
    quantity = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.product.name} (x{self.quantity})"

# Invoice Model
class Invoice(models.Model):
    order = models.OneToOneField(Order, on_delete=models.CASCADE, related_name="invoice")
    invoice_file = models.FileField(upload_to="invoices/")
    generated_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Invoice for Order {self.order.id}"

# Chatbot Interaction Model
class ChatbotInteraction(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="chat_interactions")
    message = models.TextField()
    response = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Interaction by {self.user.username} at {self.timestamp}"