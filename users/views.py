from django.shortcuts import render
from django.views.generic import CreateView
from django.urls import reverse_lazy
from .forms import CustomUserCretaionForm

class SignUpView(CreateView):
    form_class = CustomUserCretaionForm
    success_url = reverse_lazy('login')
    template_name = 'registration/register.html'
