from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Address

# Register your models here.

@admin.register(Address)
class AddressAdmin(admin.ModelAdmin):
    list_display = ('name', 'user', 'city', 'country', 'is_default')
    list_filter = ('is_default', 'country')