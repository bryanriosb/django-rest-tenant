from django.urls import path, include
from .views import (
    user_api_view, user_detail_api_view, VerifyEmailGenericAPIView, PasswordTokenCheckAPIView,
    RequestPasswordResetGenericAPIView, SetNewPasswordGenericAPIView
)

urlpatterns = [
    path('', user_api_view, name='users'),
    path('details/<int:pk>/', user_detail_api_view, name='users-detail'),
    path('email-verify/<uid64>/<token>/', VerifyEmailGenericAPIView.as_view(), name='email-verify'),
    path('request-reset-password/', RequestPasswordResetGenericAPIView.as_view(), name='request-reset-password'),
    path('reset-password/<uid64>/<token>/', PasswordTokenCheckAPIView.as_view(), name='reset-password'),
    path('reset-password-complete/', SetNewPasswordGenericAPIView.as_view(), name='reset-password-complete')
]
