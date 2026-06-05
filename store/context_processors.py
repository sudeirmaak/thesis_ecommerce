from .models import Cart, Category
from django.db.models import Sum

def cart_context(request):
    cart_count = 0

    if request.user.is_authenticated:
        try:
            cart = Cart.objects.get(user=request.user)
            aggregated = cart.cartitem_set.aggregate(total=Sum('quantity'))
            cart_count = aggregated['total'] or 0

        except Cart.DoesNotExist:
            cart_count = 0

    else:
        cart_session = request.session.get('cart', {})
        cart_count = sum(item_data.get('quantity', 0) for item_data in cart_session.values())

    return {'cart_count': cart_count}

def global_categories(request):
    return {
        'categories': Category.objects.all()
    }
