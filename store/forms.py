from django import forms
from .models import Order  

class CheckoutForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ('first_name', 'last_name', 'email', 'phone_number', 'country', 'city', 'street_address', 'postal_code', 'shipping_method')

        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control border-secondary p-2', 'placeholder': 'John'}),

            'last_name': forms.TextInput(attrs={'class': 'form-control border-secondary p-2', 'placeholder': 'Smith'}),

            'email': forms.EmailInput(attrs={
                'class': 'form-control border-secondary p-2',
                'placeholder': 'you@example.com',
            }),

            'phone_number': forms.TextInput(attrs={'class': 'form-control border-secondary py-2 phone-mask'}),

            'city': forms.TextInput(attrs={'class': 'form-control border-secondary p-2', 'placeholder': 'Warsaw'}),

            'street_address': forms.TextInput(attrs={'class': 'form-control border-secondary p-2', 'placeholder': 'Piotrkowska 123, Apt. 4'}),

            'postal_code': forms.TextInput(attrs={
                'class': 'form-control border-secondary p-2 postal-mask',
                'placeholder': '12-345',
            }),

            'shipping_method': forms.RadioSelect(attrs={'class': 'form-check-input'})
        }