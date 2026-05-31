from django.contrib import admin
from .models import Category, Product, Cart, CartItem, Order, OrderItem, Subscription, Review

# Register your models here.

admin.site.register(Review)

@admin.register(Category)
class AdminCategory(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name', )}

@admin.register(Product)
class AdminProduct(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name', )}
    list_display = ('name', 'price', 'category')

class CartItemInline(admin.TabularInline):
    model = CartItem
    extra = 0

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0

@admin.register(Order)
class AdminOrder(admin.ModelAdmin):
    list_display = ('id', 'user', 'first_name', 'last_name', 'total_amount', 'status', 'created_at')
    list_filter = ('status', 'created_at')
    inlines = [OrderItemInline]

@admin.register(Cart)
class AdminCart(admin.ModelAdmin):
    list_display = ('id', 'user', 'created_at')
    inlines = [CartItemInline]

@admin.register(Subscription)
class AdminSubscription(admin.ModelAdmin):
    list_display = ('id', 'user', 'product', 'status', 'frequency', 'next_delivery_date')
    list_filter = ('status', 'frequency')