from .models import Cart

def cart_context(request):
    cart_count = 0

    if request.user.is_authenticated:
        try:
            cart = Cart.objects.get(user=request.user)
            cart_count = sum(item.quantity for item in cart.cartitem.set_all())

        except Cart.DoesNotExist:
            cart_count = 0

    return {'cart_count' : cart_count}

# only for logged in user add guest user logic later