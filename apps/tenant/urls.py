# Django
from django.urls import include, path
from django_tenants.utils import schema_context

# Django REST Framework
from rest_framework.routers import DefaultRouter

# Views
from . import views

router = DefaultRouter()
router.register(r'clients', views.ClientViewSet, basename='clients')
router.register(r'domains', views.DomainViewSet, basename='domains')
router.register(r'accounts', views.AccountViewSet, basename='accounts')

urlpatterns = [
    path('', include(router.urls))
]