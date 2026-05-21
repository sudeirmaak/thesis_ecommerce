from django.urls import path
from .views import ProductListView, ProductDetailView, add_to_cart, cart_summary

urlpatterns = [
    path('shop/', ProductListView.as_view(), name='product_list'),
    path('shop/<slug:slug>', ProductDetailView.as_view(), name='product_detail'),
    path('add-to-cart/<int:product_id>/', add_to_cart, name='add_to_cart'),
    path('cart/',cart_summary, name='cart_summary')
    ]