from django.contrib import admin
from django.urls import path, include, re_path
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from django.conf import settings
from django.conf.urls.static import static

from apps.users.api.views import LoginAPIView, LogoutAPIView, UserTokenAPIView


schema_view = get_schema_view(
   openapi.Info(
      title="REST TENANT API",
      default_version='v1',
      description="Documentación AUBLO API",
      terms_of_service="https://www.google.com/policies/terms/",
      contact=openapi.Contact(email="bryanriosb01@gmail.com"), 
      license=openapi.License(name="CLUF License"),
   ),
   public=False,
   permission_classes=(permissions.IsAdminUser,),
)

urlpatterns = [
    re_path(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path('', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    path('admin/', admin.site.urls),
    path('auth/v1/login/', LoginAPIView.as_view(), name="login"),
    path('auth/v1/logout/', LogoutAPIView.as_view(), name="logout"),
    path('auth/v1/users/', include('apps.users.api.urls')),
    path('refresh/token/', UserTokenAPIView.as_view(), name="refresh-token"),
    path('api/v1/products/', include('apps.products.api.urls')),


] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

handler401 = 'apps.base.views.error401'
handler404 = 'apps.base.views.error404'
handler500 = 'apps.base.views.error500'
