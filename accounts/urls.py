from django.urls import path
from .views import (UserRegistration, UserLogin, UserChangePasswordView, ResetPasswordConfirmView,
                    ResetPasswordValidateView, ResetPasswordTokenView, UserProfile, DeliveryBoyRegistration)

urlpatterns = [
    path('user_register/', UserRegistration.as_view(), name='register'),
    path('delivery_boy_register/', DeliveryBoyRegistration.as_view(), name='register'),
    path('login/', UserLogin.as_view(), name='login'),
    path('', UserProfile.as_view({'get': 'list'}), name='users'),
    path('change_password/', UserChangePasswordView.as_view(), name='change_password'),
    path('validate/', ResetPasswordValidateView.as_view()),
    path('password_reset/confirm/', ResetPasswordConfirmView.as_view(), name="password-reset-confirm"),
    path('password_reset/', ResetPasswordTokenView.as_view()),
    ]
