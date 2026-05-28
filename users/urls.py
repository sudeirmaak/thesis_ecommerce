from django.urls import path, reverse_lazy
from . import views
from django.contrib.auth.views import LogoutView
from django.contrib.auth import views as auth_views
from .forms import CustomPasswordResetForm, CustomSetPasswordForm

app_name = 'users'

urlpatterns = [
    path('register/', views.SignUpView.as_view(), name='register'),
    path('login/', views.CustomLoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),

    path('profile/', views.ProfileView.as_view(), name='profile'),
    path('profile/orders/', views.OrdersView.as_view(), name='orders'),
    path('profile/orders/<int:order_id>/', views.OrderDetailView.as_view(), name='order_detail'),
    path('profile/subscriptions/', views.SubscriptionsView.as_view(), name='subscriptions'),
    path('profile/settings/', views.SettingsView.as_view(), name='settings'),

    path('profile/addresses/add/', views.AddAddressView.as_view(), name='add_address'),
    path('profile/addresses/<int:address_id>/delete/', views.delete_address, name='delete_address'),
    path('profile/addresses/<int:address_id>/set-default/', views.set_default_address, name='set_default_address'),

    path('password-reset/', auth_views.PasswordResetView.as_view(
        template_name='registration/password_reset_form.html', 
        email_template_name='registration/password_reset_email.html',
        success_url=reverse_lazy('users:password_reset_done'), 
        form_class=CustomPasswordResetForm
        ), name='password_reset'),
    path('password-reset/done/', auth_views.PasswordResetDoneView.as_view(
        template_name='registration/password_reset_done.html'
        ), name='password_reset_done'),
    path('password-reset-confirm/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(
        template_name='registration/password_reset_confirm.html', 
        success_url=reverse_lazy('users:password_reset_complete'), 
        form_class=CustomSetPasswordForm
        ), name='password_reset_confirm'),
    path('password-reset-complete/', auth_views.PasswordResetCompleteView.as_view(
        template_name='registration/password_reset_complete.html'
        ),name='password_reset_complete'),
    ]