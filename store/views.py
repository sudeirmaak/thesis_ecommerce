from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, DetailView
from .models import Product, Category, Cart, CartItem

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

        return redirect('product_list')

    return redirect('product_list')

def cart_summary(request):
    cart_items = []
    grand_total = 0

    if request.user.is_authenticated:
        cart = Cart.objects.filter(user=request.user).first()

        if cart:
            items = cart.cartitem_set.all()

            for item in items:
                subtotal = item.quantity * item.product.price
                grand_total += subtotal

                item_data = {
                    'product': item.product,
                    'size': item.size,
                    'grind': item.grind,
                    'quantity': item.quantity,
                    'purchase_option': item.purchase_option,
                    'subtotal': subtotal,
                    'item_id': item.id
                }

                cart_items.append(item_data)

    else:
        cart_session = request.session.get('cart', {})

        for key , item_data in cart_session.items():
            product = get_object_or_404(Product, id= item_data['product_id'])

            subtotal = item_data['quantity'] * product.price
            grand_total += subtotal

            new_item = {
                    'product': product,
                    'size': item_data['size'],
                    'grind': item_data['grind'],
                    'quantity': item_data['quantity'],
                    'purchase_option': item_data['purchase_option'],
                    'subtotal': subtotal,
                    'item_id': key
                }
            
            cart_items.append(new_item)
    
    context = {
        'cart_items': cart_items,
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
