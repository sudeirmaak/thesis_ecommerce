from django.urls import path
from .views import ProductListView, ProductDetailView, add_to_cart, cart_summary, remove_from_cart, update_cart

urlpatterns = [
    path('', ProductListView.as_view(), name='product_list'),
    path('product/<slug:slug>', ProductDetailView.as_view(), name='product_detail'),
    path('add-to-cart/<int:product_id>/', add_to_cart, name='add_to_cart'),
    path('cart/',cart_summary, name='cart_summary'),
    path('remove/<str:item_id>/', remove_from_cart, name='remove_from_cart'),
    path('update/<str:item_id>/', update_cart, name='update_cart')
    ]