from django.contrib import admin
from .models import Category, Product

# Register your models here.

@admin.register(Category)
class AdminCategory(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name', )}

@admin.register(Product)
class AdminProduct(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name', )}
    list_display = ('name', 'price', 'category')

