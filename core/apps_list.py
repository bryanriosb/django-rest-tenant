BEFORE_DJANGO_APPS = (
    'tenant_schemas',
)

DJANGO_APPS = (
    'django.contrib.contenttypes',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.gis',
)

LOCAL_APPS = (
    'apps.tenant',
    'apps.users',
    'apps.prueba',
    'apps.base',
    'apps.products',
)

THIRD_PARTY_APPS = (
    'rest_framework',
    'rest_framework.authtoken',
    'simple_history',
    'drf_yasg',
)

SHARED_APPS = (
    'tenant_schemas',
    'apps.tenant',
    'apps.prueba',
    'apps.users',
) + DJANGO_APPS

TENANT_APPS = (
    'django.contrib.contenttypes',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.sessions',
    'django.contrib.gis',
    'rest_framework',
    'rest_framework.authtoken',
    'simple_history',
    'drf_yasg',
) + LOCAL_APPS


INSTALLED_APPS = BEFORE_DJANGO_APPS + DJANGO_APPS + LOCAL_APPS + THIRD_PARTY_APPS
