from django.db import models
from django.conf import settings

STATUS_CHOICES_ORDER = [
    ("P", "Pending"),
    ("A", "Approved"),
    ("S", "Shipped"),
    ("D", "Delivered"),
    ("C", "Cancelled")
]

STATUS_CHOICES_SUBSCRIPTION = [
    ("P", "Paused"),
    ("A", "Active"),
    ("C", "Cancelled")
]

FREQUENCY_CHOICES_SUBSCRIPTION = [
    ("W", "Weekly"),
    ("M", "Monthly")
]

class Category(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField(unique=True)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name_plural = 'Categories'

class Product(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    slug = models.SlugField(unique=True)
    price = models.DecimalField(max_digits=7, decimal_places=2)
    stock = models.PositiveIntegerField()
    image = models.ImageField(upload_to='images/')
    description = models.TextField(blank=True)
    tags = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

class Cart(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Cart {self.id} - {self.user.username}"

class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    size = models.CharField(max_length=50, blank=True)
    grind = models.CharField(max_length=50, blank=True)
    purchase_option = models.CharField(max_length=50, blank=True)

    def __str__(self):
        return f"{self.quantity}x {self.product.name} (Cart {self.cart.id})"

class Order(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)
    full_name = models.CharField(max_length=255)
    email = models.EmailField(max_length=255)
    street_address = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    postal_code = models.CharField(max_length=255)
    country = models.CharField(max_length=255)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=1, choices=STATUS_CHOICES_ORDER, default="P")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        if self.user:
            return f"Order {self.id} by {self.user.username}"
        else: 
            return f"Order {self.id} by Deleted User"

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    price = models.DecimalField(max_digits=7, decimal_places=2)
    quantity = models.PositiveIntegerField()
    size = models.CharField(max_length=50, blank=True)
    grind = models.CharField(max_length=50, blank=True)
    purchase_option = models.CharField(max_length=50, blank=True)
    
    def __str__(self):
        if self.product:
            return f"{self.quantity}x {self.product.name} (Order {self.order.id})"
        else:
            return f"{self.quantity}x Deleted Product (Order {self.order.id})"
    
    def get_cost(self):
        return self.price * self.quantity
    
class Subscription(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    original_order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True)
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    status = models.CharField(max_length=1, choices=STATUS_CHOICES_SUBSCRIPTION, default="P")
    frequency = models.CharField(max_length=1, choices=FREQUENCY_CHOICES_SUBSCRIPTION, default="W")
    next_delivery_date = models.DateField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        if self.product:
            return f"Subscription: {self.product.name} for {self.user.username}"
        else:
            return f"Subscription: Deleted Product for {self.user.username}"

