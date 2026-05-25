from django.urls import path
from .views import SignUpView, CustomLoginView, ProfileView, OrdersView, SubscriptionsView, SettingsView
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth import views as auth_views
from .forms import CustomPasswordResetForm, CustomSetPasswordForm

app_name = 'users'

urlpatterns = [
    path('register/', SignUpView.as_view(), name='register'),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('profile/', ProfileView.as_view(), name='profile'),
    path('profile/orders/', OrdersView.as_view(), name='orders'),
    path('profile/subscriptions/', SubscriptionsView.as_view(), name='subscriptions'),
    path('profile/settings/', SettingsView.as_view(), name='settings'),
    path('password-reset/', auth_views.PasswordResetView.as_view(template_name='registration/password_reset_form.html', 
        success_url='/users/password-reset/done/', form_class=CustomPasswordResetForm), name='password_reset'),
    path('password-reset/done/', auth_views.PasswordResetDoneView.as_view(template_name='registration/password_reset_done.html'), 
        name='password_reset_done'),
    path('password-reset-confirm/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(
        template_name='registration/password_reset_confirm.html', 
        success_url='/users/password-reset-complete/', form_class=CustomSetPasswordForm), name='password_reset_confirm'),
    path('password-reset-complete/', auth_views.PasswordResetCompleteView.as_view(template_name='registration/password_reset_complete.html'),
        name='password_reset_complete')
    ]