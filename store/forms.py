from django import forms
from .models import Order, Review 

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

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['rating', 'comment']

        widgets = {
            'rating': forms.Select(attrs={'class': 'form-select border-dark w-auto mb-3'}),
            'comment': forms.Textarea(attrs={'class': 'form-control border-dark',
                                             'rows': 4,
                                             'placeholder': 'Share you thoughts...'}),
        }