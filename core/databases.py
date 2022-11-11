import os
from dotenv import load_dotenv

load_dotenv()

DATABASES = {
    'default': {
        'ENGINE': 'django_tenants.postgresql_backend',
        'NAME': os.getenv('POSTGRES_DB'),
        'USER': os.getenv('POSTGRES_USER'),
        'PASSWORD': os.getenv('POSTGRES_PASSWORD'),
        'HOST': os.getenv('POSTGRES_HOST'),
        'PORT': os.getenv('POSTGRES_PORT', 5432),
    }
}

DATABASE_ROUTERS = (
    'django_tenants.routers.TenantSyncRouter',
)

DEFAULT_FILE_STORAGE = 'django_tenants.storage.TenantFileSystemStorage'

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# Tenant Config
TENANT_MODEL = "tenant.Client"
TENANT_DOMAIN_MODEL = "tenant.Domain"
