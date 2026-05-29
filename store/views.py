from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.views.generic import ListView, DetailView, TemplateView
from django.views import View
from .models import Product, Category, Cart, CartItem, Order, OrderItem, Subscription
from users.models import Address
from .forms import CheckoutForm
from decimal import Decimal

class HomeView(TemplateView):
    template_name = 'store/home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['hero_top'] = Product.objects.filter(slug='sumatra-mandheling-dark').first()
        context['single_origin'] = Product.objects.filter(category__slug='single-origin')
        context['blends'] = Product.objects.filter(category__slug='blends')
        context['decaf'] = Product.objects.filter(category__slug='decaf')
        context['hero_bottom'] = Product.objects.filter(slug='baratza-encore-burr-grinder').first()
        context['brewing_equipment'] = Product.objects.filter(category__slug='brewing-equipment')

        return context

class ProductListView(ListView):
    model = Product
    template_name = 'store/product_list.html'
    context_object_name = 'products'

class ProductDetailView(DetailView):
    model = Product
    template_name = 'store/product_detail.html'
    context_object_name = 'product'

def add_to_cart(request, product_id):
    if request.method == 'POST':
        product = get_object_or_404(Product, id= product_id)
        size = request.POST.get('size')
        grind = request.POST.get('grind')
        purchase_option = request.POST.get('purchase')
        quantity = int(request.POST.get('quantity', 1))

        if request.user.is_authenticated:
            cart, created = Cart.objects.get_or_create(user = request.user)

            cart_item, item_created = CartItem.objects.get_or_create(
                cart = cart,
                product = product,
                size = size,
                grind = grind,
                purchase_option = purchase_option
            )
            if not item_created:
                cart_item.quantity += quantity
            else:
                cart_item.quantity = quantity
            cart_item.save()

        else:
            cart_session = request.session.get('cart')
            if cart_session is None:
                cart_session = {}

            item_key = f"{product_id}_{size}_{grind}_{purchase_option}"

            if item_key in cart_session:
                cart_session[item_key]['quantity'] += quantity
            else:
                cart_session[item_key] = {
                    'product_id': product_id,
                    'size': size,
                    'grind': grind,
                    'purchase_option': purchase_option,
                    'quantity': quantity
                }

            request.session['cart'] = cart_session
            request.session.modified = True

        messages.success(request, f"{product.name} was successfully added to your cart.")

        return redirect('product_detail', slug=product.slug)

    return redirect('product_list')

def cart_summary(request):
    cart_items = []
    cart_subtotal = 0

    if request.user.is_authenticated:
        cart = Cart.objects.filter(user=request.user).first()

        if cart:
            items = cart.cartitem_set.all()

            for item in items:
                subtotal = item.get_subtotal()
                cart_subtotal += subtotal

                item_data = {
                    'product': item.product,
                    'size': item.size,
                    'grind': item.grind,
                    'quantity': item.quantity,
                    'purchase_option': item.purchase_option,
                    'unit_price': item.get_unit_price(),
                    'subtotal': subtotal,
                    'item_id': item.id
                }

                cart_items.append(item_data)

    else:
        cart_session = request.session.get('cart', {})

        for key , item_data in cart_session.items():
            product = get_object_or_404(Product, id= item_data['product_id'])

            size_price = product.get_size_price(item_data['size'])
            subtotal = item_data['quantity'] * size_price

            new_item = {
                    'product': product,
                    'size': item_data['size'],
                    'grind': item_data['grind'],
                    'quantity': item_data['quantity'],
                    'purchase_option': item_data['purchase_option'],
                    'unit_price': size_price,
                    'subtotal': subtotal,
                    'item_id': key
                }
            
            cart_items.append(new_item)
    
    shipping_cost = 0
    grand_total = cart_subtotal + shipping_cost

    context = {
        'cart_items': cart_items,
        'cart_subtotal': cart_subtotal,
        'grand_total': grand_total
    }

    return render(request, 'store/cart.html', context)

def remove_from_cart(request, item_id):
    if request.user.is_authenticated:
        CartItem.objects.filter(id=item_id, cart__user=request.user).delete()
    else:
        cart_session = request.session.get('cart', {})
        
        if item_id in cart_session:
            del cart_session[item_id]
            request.session['cart'] = cart_session
            request.session.modified = True
    
    messages.warning(request, "Item removed from your cart.")
    return redirect('cart_summary')

def update_cart(request, item_id):
    if request.method == 'POST':
        try:
            quantity = int(request.POST.get('quantity'))
            if quantity < 1:
                quantity = 1
        except(ValueError, TypeError):
            quantity = 1
            
        if request.user.is_authenticated:
            item = CartItem.objects.filter(id=item_id, cart__user=request.user).first()
            if item:
                item.quantity = quantity
                item.save()

        else:
            cart_session = request.session.get('cart', {})
            if item_id in cart_session:
                cart_session[item_id]['quantity'] = quantity
                request.session['cart'] = cart_session
                request.session.modified = True

    return redirect('cart_summary')

class CheckoutView(LoginRequiredMixin, View):
    def get(self, request):
        cart = Cart.objects.filter(user=request.user).first()

        if not cart or not cart.cartitem_set.exists():
            messages.error(request, "Your cart is empty. Please add an item before checking out.")
            return redirect('cart_summary')
        
        total_price = 0
        cart_items = cart.cartitem_set.all()

        for item in cart_items:
            total_price += item.get_unit_price() * item.quantity

        default_shipping = Decimal('5.00')
        grand_total = total_price + default_shipping

        initial_data = {
            'email': request.user.email,
        }

        default_address = Address.objects.filter(user=request.user, is_default=True).first()

        if default_address:
            initial_data.update({
                'first_name':default_address.first_name,
                'last_name':default_address.last_name,
                'phone_number':default_address.phone_number,
                'street_address':default_address.street_address,
                'city':default_address.city,
                'postal_code':default_address.postal_code,
                'country':default_address.country,
            })
        else:
            initial_data.update ({
                'first_name': request.user.first_name,
                'last_name': request.user.last_name,
                'phone_number': request.user.phone_number,
            })

        form = CheckoutForm(initial=initial_data)

        context = {
            'form': form,
            'cart_items': cart_items,
            'total_price': total_price,
            'shipping_cost': default_shipping,
            'grand_total': grand_total
        }

        return render(request, 'store/checkout.html', context)
    
    def post(self, request):
        cart = Cart.objects.filter(user=request.user).first()

        if not cart or not cart.cartitem_set.exists():
            messages.error(request, "Your cart is empty. Please add an item before checking out.")
            return redirect('cart_summary')
        
        total_price = 0
        cart_items = cart.cartitem_set.all()

        for item in cart_items:
            total_price += item.get_unit_price() * item.quantity

        form = CheckoutForm(request.POST)

        if form.is_valid():
            order = form.save(commit=False)
            order.user = request.user

            if order.shipping_method == 'express':
                order.shipping_cost = Decimal(15.00)
            else:
                order.shipping_cost = Decimal(5.00)

            grand_total = total_price + order.shipping_cost

            order.total_amount = grand_total
            order.save()

            for item in cart_items:
                OrderItem.objects.create(
                    order = order,
                    product = item.product,
                    price = item.get_unit_price(),
                    quantity = item.quantity,
                    size = item.size,
                    grind = item.grind,
                    purchase_option = item.purchase_option
                )

            cart.cartitem_set.all().delete()

            return redirect('order_success', order_id = order.id)
        
        context = {
            'form': form,
            'cart_items': cart_items,
            'total_price': total_price
        }

        return render(request, 'store/checkout.html', context)
    
def order_success(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)

    context = {
        'order': order
    }

    return render(request, 'store/order_success.html', context)