from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, PasswordResetForm, SetPasswordForm
from django.contrib.auth import get_user_model
from django import forms
from .models import Address
import re

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = get_user_model()
        fields = ('first_name', 'last_name', 'username', 'email')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['first_name'].required = True
        self.fields['last_name'].required = True
        self.fields['username'].required = True
        self.fields['email'].required = True

        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'

class CustomLoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'

class CustomPasswordResetForm(PasswordResetForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'

class CustomSetPasswordForm(SetPasswordForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'

class CustomUserUpdateForm(forms.ModelForm):
    class Meta:
        model = get_user_model()
        fields = ('first_name', 'last_name', 'email', 'phone_number')

    def __init__(self, *args, **kwargs):
        super().__init__( *args, **kwargs)

        self.fields['first_name'].required = True
        self.fields['last_name'].required = True
        self.fields['email'].required = True
        self.fields['phone_number'].required = True

        for field_name, field in self.fields.items():
            if field_name == 'email':
                field.widget.attrs.update({'class': 'form-control border-secondary p-2', 'list': 'email-suggestions'})
            elif field_name == 'phone_number':
                field.widget.attrs.update({'class': 'form-control border-secondary py-2 phone-mask'})
            else:
                field.widget.attrs['class'] = 'form-control border-secondary p-2'

    def clean_phone_number(self):
        phone = self.cleaned_data.get('phone_number')

        if phone:
            if re.search('[a-zA-Z]', phone):
                raise forms.ValidationError("Please enter a valid phone number.")
            
            if len(re.sub(r'\D', '', phone)) < 7:
                raise forms.ValidationError("Please enter a valid phone number.")
            
        return phone
    
class AddressForm(forms.ModelForm):
    class Meta:
        model = Address
        fields = ('name', 'first_name', 'last_name', 'phone_number', 'street_address', 'city', 'postal_code', 'country', 'is_default')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field_name, field in self.fields.items():
            if field_name == 'is_default':
                field.widget.attrs['class'] = 'form-check-input border-secondary'
            elif field_name == 'postal_code':
                field.widget.attrs.update({'class': 'form-control border-secondary p-2 postal-mask', 'placeholder': '12-345'})
            elif field_name == 'phone_number':
                field.widget.attrs.update({'class': 'form-control border-secondary py-2 phone-mask'})
            else:
                field.widget.attrs['class'] = 'form-control border-secondary p-2'
