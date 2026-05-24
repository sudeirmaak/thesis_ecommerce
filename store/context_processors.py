from .models import Cart

def cart_context(request):
    cart_count = 0

    if request.user.is_authenticated:
        try:
            cart = Cart.objects.get(user=request.user)
            cart_count = sum(item.quantity for item in cart.cartitem_set.all())

        except Cart.DoesNotExist:
            cart_count = 0

    else:
        cart_session = request.session.get('cart', {})
        for key, item_data in cart_session.items():
            cart_count += item_data['quantity']

    return {'cart_count': cart_count}
