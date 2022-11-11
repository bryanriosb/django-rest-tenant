# Django
from django.urls import include, path

# Django REST Framework
from rest_framework.routers import DefaultRouter

# Views
from . import  views

router = DefaultRouter()
router.register(r'users', views.UserViewSet, basename='users')
router.register(r'email_verification', views.VerificationEmailViewSet, basename='email_verification')
# router.register(r'sign_in', views.SignInViewSet, basename='sign_in')
# router.register(r'sign_out', views.SignOutViewSet, basename='sign_out')
# router.register(r'refresh_token', views.RefreshTokenViewSet, basename='refresh_token')
router.register(r'request_reset_password', views.RequestPasswordResetViewSet, basename='request_reset_password')
router.register(r'reset_password', views.SetNewPasswordViewSet, basename='reset_password')


urlpatterns = [
    path('', include(router.urls)),
]