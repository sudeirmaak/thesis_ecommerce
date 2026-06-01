from django.urls import path
from . import views

urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('shop/', views.ProductListView.as_view(), name='product_list'),
    path('category/<slug:slug>/', views.CategoryView.as_view(), name='category_products'),
    path('search/', views.SearchView.as_view(), name='search'),
    path('product/<slug:slug>', views.ProductDetailView.as_view(), name='product_detail'),
    path('submit-review/<int:product_id>/', views.submit_review, name='submit_review'),
    path('add-to-cart/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('cart/',views.cart_summary, name='cart_summary'),
    path('remove/<str:item_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('update/<str:item_id>/', views.update_cart, name='update_cart'),
    path('webhook/stripe/', views.stripe_webhook, name='stripe_webhook'),
    path('checkout/', views.CheckoutView.as_view(), name='checkout'),
    path('checkout/success/<int:order_id>/', views.order_success, name='order_success')
    ]