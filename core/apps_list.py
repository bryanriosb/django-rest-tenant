BEFORE_DJANGO_APPS = (
    'django_tenants',
    'daphne',
)

DJANGO_APPS = (
    'django.contrib.contenttypes',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
)

LOCAL_APPS = (
    'apps.tenant',
    'apps.common',
    'apps.users',
    'apps.ipfs',
)

THIRD_PARTY_APPS = (
    'rest_framework',
    'rest_framework.authtoken',
    'rest_framework_simplejwt',

    'drf_spectacular',
    'drf_spectacular_sidecar',

    'corsheaders',
    'django_celery_results',
    'django_celery_beat',
)

SHARED_APPS = (
    'django_tenants',

    'apps.tenant',
    'apps.common',

    'rest_framework',
    'rest_framework.authtoken',
    'rest_framework_simplejwt',

    'drf_spectacular',
    'drf_spectacular_sidecar',
    'django_celery_results',
    'django_celery_beat',
) + DJANGO_APPS

TENANT_APPS = (
    'django.contrib.contenttypes',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.sessions',
    'django_celery_results',
    'django_celery_beat',
) + LOCAL_APPS


INSTALLED_APPS = BEFORE_DJANGO_APPS + DJANGO_APPS + LOCAL_APPS + THIRD_PARTY_APPS
