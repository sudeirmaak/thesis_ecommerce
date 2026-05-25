from django.shortcuts import render
from django.views.generic import CreateView
from django.urls import reverse_lazy
from django.contrib.auth.views import LoginView
from store.models import Cart, CartItem, Product
from .forms import CustomUserCreationForm, CustomLoginForm

class SignUpView(CreateView):
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('users:login')
    template_name = 'registration/register.html'

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
