from django.urls import path
from . import views

urlpatterns = [
    # main navigation
    path('', views.HomeView.as_view(), name='home'),
    path('search/', views.SearchView.as_view(), name='search'),

    # product catalog
    path('shop/', views.ProductListView.as_view(), name='product_list'),
    path('category/<slug:slug>/', views.CategoryView.as_view(), name='category_products'),
    path('product/<slug:slug>/', views.ProductDetailView.as_view(), name='product_detail'),
    path('submit-review/<int:product_id>/', views.submit_review, name='submit_review'),

    # cart management 
    path('cart/', views.cart_summary, name='cart_summary'),
    path('add-to-cart/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('remove/<str:item_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('update/<str:item_id>/', views.update_cart, name='update_cart'),

    # checkout and webhook
    path('checkout/', views.CheckoutView.as_view(), name='checkout'),
    path('checkout/success/<int:order_id>/', views.order_success, name='order_success'),
    path('webhook/stripe/', views.stripe_webhook, name='stripe_webhook'),
    ]