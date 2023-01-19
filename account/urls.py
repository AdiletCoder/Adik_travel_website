from django.urls import path, include
from django.contrib.auth.views import LogoutView
from account.views import RegisterView, SignInView, profile, change_password, ResetPasswordView, add_service

from django.contrib.auth import views as auth_views

urlpatterns = [
    path('signup/', RegisterView.as_view(), name='register'),
    path('login/', SignInView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('myprofile/', profile, name='profile'),
    path('change-password/', change_password, name='change_password'),
    path('password-reset-confirm/<uidb64>/<token>/',
         auth_views.PasswordResetConfirmView.as_view(template_name='account/reset_password_confirm.html'),
         name='password_reset_confirm'),
    path('password-reset-complete/',
         auth_views.PasswordResetCompleteView.as_view(template_name='account/password_reset_complete.html'),
         name='password_reset_complete'),
    path('password-reset/', ResetPasswordView.as_view(), name='password_reset'),
    path('myprofile/service/', add_service, name='g-add_service'),
]
