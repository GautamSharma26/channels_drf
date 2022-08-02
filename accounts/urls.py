from django.urls import path
from .views import (UserRegistration, UserLogin, UserChangePasswordView, ResetPasswordConfirmView,
                    ResetPasswordValidateView, ResetPasswordTokenView, UserProfile)

urlpatterns = [
    path('register/', UserRegistration.as_view(), name='register'),
    path('login/', UserLogin.as_view(), name='login'),
    path('', UserProfile.as_view({'get': 'list'}), name='users'),
    path('change_password/', UserChangePasswordView.as_view(), name='change_password'),
    path('validate/', ResetPasswordValidateView.as_view()), # 2
    path('password_reset/confirm/', ResetPasswordConfirmView.as_view(), name="password-reset-confirm"), # 3
    path('password_reset/', ResetPasswordTokenView.as_view()),
    ]