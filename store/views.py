from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.generic import ListView, DetailView, TemplateView
from django.views import View
from django.utils import timezone
from django.db.models import Q
from .models import Product, Category, Cart, CartItem, Order, OrderItem, Subscription, Review
from users.models import Address
from .forms import CheckoutForm, ReviewForm
from .recommender import get_recommendations
from decimal import Decimal
from datetime import timedelta
from django.conf import settings
from django.urls import reverse
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
import stripe

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

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['current_category'] = None
        return context  

class ProductDetailView(DetailView):
    model = Product
    template_name = 'store/product_detail.html'
    context_object_name = 'product'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['review_form'] = ReviewForm()

        current_product = self.object 
        recommended = get_recommendations(current_product.id, top_n=4)

        if not recommended:
            recommended = Product.objects.filter(category=current_product.category).exclude(id=current_product.id).order_by('?')[:4]

        context['recommended_products'] = recommended
        return context  

class CategoryView(ListView):
    model = Product
    template_name = 'store/product_list.html'
    context_object_name = 'products'

    def get_queryset(self):
        category_slug = self.kwargs.get('slug')
        category = get_object_or_404(Category, slug=category_slug)
        return Product.objects.filter(category=category)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['current_category'] = get_object_or_404(Category, slug=self.kwargs.get('slug'))
        return context
    
class SearchView(ListView):
    model = Product
    template_name = 'store/product.list.html'
    context_object_name = 'products'

    def get_queryset(self):
        query = self.request.GET.get('q')

        if query:
            return Product.objects.filter(
                Q(name__icontains = query) |
                Q(description__icontains = query) |
                Q(tags__icontains = query) |
                Q(category__name__icontains=query)
            ).distinct()
        
        return Product.objects.none()
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['search_query'] = self.request.GET.get('q', '')
        context['current_category'] = None
        return context

def add_to_cart(request, product_id):
    if request.method == 'POST':
        product = get_object_or_404(Product, id= product_id)
        size = request.POST.get('size')
        grind = request.POST.get('grind')
        purchase_option = request.POST.get('purchase')
        quantity = int(request.POST.get('quantity', 1))
        frequency = request.POST.get('frequency')

        if request.user.is_authenticated:
            cart, created = Cart.objects.get_or_create(user = request.user)

            cart_item, item_created = CartItem.objects.get_or_create(
                cart = cart,
                product = product,
                size = size,
                grind = grind,
                purchase_option = purchase_option,
                frequency = frequency
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
                    'quantity': quantity,
                    'frequency': frequency
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
                    'frequency': item.frequency,
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

            if item_data.get('purchase_option') == 'subscribe':
                size_price = size_price * Decimal('0.90')

            subtotal = item_data['quantity'] * size_price

            cart_subtotal += subtotal

            new_item = {
                    'product': product,
                    'size': item_data['size'],
                    'grind': item_data['grind'],
                    'quantity': item_data['quantity'],
                    'purchase_option': item_data['purchase_option'],
                    'frequency': item_data.get('frequency', 'M'),
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
    login_url = 'users:login'

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

        user_addresses = Address.objects.filter(user=request.user)

        context = {
            'form': form,
            'cart_items': cart_items,
            'total_price': total_price,
            'shipping_cost': default_shipping,
            'grand_total': grand_total,
            'user_addresses': user_addresses,
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
            order.shipping_cost = Decimal('15.00') if order.shipping_method == 'express' else Decimal('5.00')
            grand_total = total_price + order.shipping_cost
            order.total_amount = grand_total
            order.save()

            stripe.api_key = settings.STRIPE_SECRET_KEY
            line_items = []

            for item in cart_items:
                OrderItem.objects.create(
                    order = order,
                    product = item.product,
                    price = item.get_unit_price(),
                    quantity = item.quantity,
                    size = item.size,
                    grind = item.grind,
                    purchase_option = item.purchase_option,
                    frequency = item.frequency
                )

                line_items.append({
                    'price_data': {
                        'currency': 'usd',
                        'unit_amount': int(item.get_unit_price() * 100),
                        'product_data': {
                            'name': f"{item.product.name} ({item.size} - {item.grind})",
                        },
                    },
                    'quantity': item.quantity,
                })

            line_items.append({
                'price_data': {
                    'currency': 'usd',
                    'unit_amount': int(order.shipping_cost * 100),
                    'product_data': {
                        'name': 'Shipping',
                    },
                },
                'quantity': 1,
            })

            try:
                checkout_session = stripe.checkout.Session.create(
                    payment_method_types=['card'],
                    line_items=line_items,
                    mode='payment',
                    customer_email=order.email,
                    client_reference_id=order.id, # Critical: Ties Stripe back to your database!
                    success_url=request.build_absolute_uri(reverse('order_success', args=[order.id])),
                    cancel_url=request.build_absolute_uri(reverse('cart_summary')),
                )
                return redirect(checkout_session.url, code=303)
            
            except Exception as e:
                messages.error(request, "There was an error connecting to the payment processor. Please try again.")
                return redirect('cart_summary')
        
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

@login_required(login_url='users:login')
def submit_review(request, product_id):

    product = get_object_or_404(Product, id=product_id)

    if request.method == 'POST':

        if Review.objects.filter(user=request.user, product=product).exists():
            messages.warning(request, "You have already reviewed this product.")
            return redirect('product_detail', slug=product.slug)
        
        form = ReviewForm(request.POST)

        if form.is_valid():
            review = form.save(commit=False)
            review.product = product
            review.user = request.user
            review.save()
            messages.success(request, "Thank you for your review!")

    return redirect('product_detail', slug=product.slug)

@csrf_exempt
def stripe_webhook(request):
    payload = request.body
    sig_header = request.META.get('HTTP_STRIPE_SIGNATURE')
    event = None

    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, settings.STRIPE_WEBHOOK_SECRET
        )
    except ValueError as e:
        # Invalid payload
        return HttpResponse(status=400)
    except stripe.error.SignatureVerificationError as e:
        # Invalid signature (Hack attempt!)
        return HttpResponse(status=400)

    if event['type'] == 'checkout.session.completed':
        session = event['data']['object']
        
        order_id = session.client_reference_id

        if order_id:
            try:
                order = Order.objects.get(id=order_id)
                
                order.status = 'A'
                order.save()

                for item in order.items.all():
                    if item.purchase_option == 'subscribe':
                        days_to_add = 7 if item.frequency == 'W' else 30
                        next_date = timezone.now().date() + timedelta(days=days_to_add)

                        Subscription.objects.create(
                            user=order.user,
                            original_order=order,
                            product=item.product,
                            quantity=item.quantity,
                            size=item.size,
                            grind=item.grind,
                            price_locked=item.price,
                            status='A',
                            frequency=item.frequency,
                            next_delivery_date=next_date
                        )

                if order.user:
                    cart = Cart.objects.filter(user=order.user).first()
                    if cart:
                        cart.cartitem_set.all().delete()

            except Order.DoesNotExist:
                pass 

    return HttpResponse(status=200)