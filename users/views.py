from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.views.generic import CreateView, TemplateView, UpdateView
from django.urls import reverse_lazy
from django.contrib.auth import login
from django.contrib.auth.views import LoginView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.http import HttpResponseRedirect
from store.models import Cart, CartItem, Product, Order
from .forms import CustomUserCreationForm, CustomLoginForm, CustomUserUpdateForm, AddressForm
from .models import Address

class SignUpView(CreateView):
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('home')
    template_name = 'registration/register.html'

    def form_valid(self, form):
        response = super().form_valid(form)

        login(self.request, self.object)

        return response

class CustomLoginView(LoginView):
    form_class = CustomLoginForm
    
    def form_valid(self, form):
        response = super().form_valid(form)
        cart_session = self.request.session.get('cart', {})

        if cart_session:
            cart, created = Cart.objects.get_or_create(user=self.request.user)

            for key, item_data in cart_session.items():
                product = Product.objects.get(id=item_data['product_id'])

                cart_item, item_created = CartItem.objects.get_or_create(
                    cart = cart,
                    product = product,
                    size = item_data['size'],
                    grind = item_data['grind'],
                    purchase_option = item_data['purchase_option']
                )

                if not item_created:
                    cart_item.quantity += item_data['quantity']
                else:
                    cart_item.quantity = item_data['quantity']

                cart_item.save()

            del self.request.session['cart']
            self.request.session.modified = True

        return response
    
class ProfileView(LoginRequiredMixin, TemplateView):
    template_name = 'users/profile.html'
    login_url = 'users:login'

class OrdersView(LoginRequiredMixin, TemplateView):
    template_name = 'users/orders.html'
    login_url = 'users:login'

    def get_context_data(self, **kwargs):

        context = super().get_context_data(**kwargs)

        context['orders'] = Order.objects.filter(user=self.request.user).order_by('-created_at')

        return context

class SubscriptionsView(LoginRequiredMixin, TemplateView):
    template_name = 'users/subscriptions.html'
    login_url = 'users:login'

class SettingsView(LoginRequiredMixin, UpdateView):
    template_name = 'users/settings.html'
    login_url = 'users:login'
    form_class = CustomUserUpdateForm
    success_url = reverse_lazy('users:settings')

    def get_object(self):
        return self.request.user
    
    def form_valid(self, form):

        if form.has_changed():
            messages.success(self.request, "Your personal details have been successfully updated!")
            return super().form_valid(form)
        else:
            messages.info(self.request, "No changes were made to your personal details.")
            return HttpResponseRedirect(self.get_success_url())
        
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['addresses'] = Address.objects.filter(user=self.request.user)
        return context


class OrderDetailView(LoginRequiredMixin, TemplateView):
    template_name = 'users/order_detail.html'
    login_url = 'users:login'

    def get_context_data(self, **kwargs):

        context = super().get_context_data(**kwargs)

        order_id = self.kwargs.get('order_id')

        order = get_object_or_404(Order, id=order_id, user=self.request.user)

        context['order'] = order

        return context
    
class AddAddressView(LoginRequiredMixin, CreateView):
    model = Address
    form_class =AddressForm
    template_name = 'users:add_address.html'
    success_url = reverse_lazy('users:settings')

    def form_valid(self, form):
        form.instance.user = self.request.user
        messages.success(self.request, "New address added successfully!")
        return super().form_valid(form)
    
@login_required
def delete_address(request, address_id):
    address = get_object_or_404(Address, id=address_id, user=request.user)
    address.delete()
    messages.success(request, "Address deleted successfully!")
    return redirect('users:settings')

@login_required
def set_default_address(request, address_id):
    address = get_object_or_404(Address, id=address_id, user=request.user)
    address.is_default = True
    address.save()
    messages.success(request, f"{address.name} is now your default address!")
    return redirect('users:settings')