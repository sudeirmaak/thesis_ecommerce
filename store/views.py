from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, DetailView
from .models import Product, Category

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

        print(f"test: {product.name}, {quantity}x, size:{size}, grind:{grind}, purchase:{purchase_option}")

        return redirect('product_list')

    return redirect('product_list')

