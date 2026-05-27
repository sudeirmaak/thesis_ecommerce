from django import forms
from .models import Order  

class CheckoutForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ('first_name', 'last_name', 'email', 'phone_number', 'country', 'city', 'street_address', 'postal_code', 'shipping_method')

        widgets = {
            'fist_name': forms.TextInput(attrs={'placeholder': 'John'}),

            'last_name': forms.TextInput(attrs={'placeholder': 'Smith'}),

            'email': forms.EmailInput(attrs={
                'placeholder': 'you@example.com',
                'list': 'email-suggestions'
            }),

            'phone_number': forms.TextInput(attrs={
                'placeholder': '+48 123 456 789',
                'pattern': r'^\+?[0-9\s]+$',
                'title': 'Enter a valid phone number (e.g. +48 123 456 789)',
                'minlength': '9',
                'maxlength': '15'
            }),

            'city': forms.TextInput(attrs={'placeholder': 'Warsaw'}),

            'street_address': forms.TextInput(attrs={'placeholder': 'Piotrkowska 123, Apt. 4'}),

            'postal_code': forms.TextInput(attrs={
                'placeholder': '12-345',
                'id': 'postal-mask'
            }),

            'shipping_method': forms.RadioSelect(attrs={'class': 'form-check-input'})
        }