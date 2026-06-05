from django.contrib import admin
from .models import Category, Product, Cart, CartItem, Order, OrderItem, Subscription, Review

# Register your models here.

# standalone model no custom columns needed 
admin.site.register(Review)

# inline models 
class CartItemInline(admin.TabularInline):
    model = CartItem
    extra = 0

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0

# admin classes
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name', )}
    search_fields = ('name',)

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name', )}
    list_display = ('name', 'price', 'category')
    list_filter = ('category',)
    search_fields = ('name', 'description')

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'first_name', 'last_name', 'total_amount', 'status', 'created_at')
    list_filter = ('status', 'created_at')
    inlines = [OrderItemInline]
    earch_fields = ('first_name', 'last_name', 'id')

@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'created_at')
    inlines = [CartItemInline]

@admin.register(Subscription)
class SubscriptionAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'product', 'status', 'frequency', 'next_delivery_date')
    list_filter = ('status', 'frequency')
    search_fields = ('product__name',)