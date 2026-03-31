from django.urls import path
from .views import ProductListView, ProductDetailView

urlpatterns = [
    path('shop/', ProductListView.as_view(), name='product_list'),
    path('shop/<slug:slug>', ProductDetailView.as_view(), name='product_detail'),
    ]