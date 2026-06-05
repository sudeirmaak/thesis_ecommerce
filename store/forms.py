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

    rating = forms.ChoiceField(
            choices=[
                (5, '⭐⭐⭐⭐⭐ (5 - Excellent)'),
                (4, '⭐⭐⭐⭐ (4 - Good)'),
                (3, '⭐⭐⭐ (3 - Average)'),
                (2, '⭐⭐ (2 - Poor)'),
                (1, '⭐ (1 - Terrible)')
            ],
            widget=forms.Select(attrs={'class': 'form-select border-dark w-auto mb-3'})
        )

    class Meta:
        model = Review
        fields = ['rating', 'comment']

        widgets = {
            'comment': forms.Textarea(attrs={'class': 'form-control border-dark',
                                             'rows': 4,
                                             'placeholder': 'Share your thoughts...'}),
        }