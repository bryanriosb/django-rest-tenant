from django.db import models
from tenant_schemas.models import TenantMixin


class Client(TenantMixin):
    name = models.CharField(max_length=500)
    is_active = models.BooleanField(default=True)
    create_at = models.DateTimeField(auto_now_add=True)

    auto_create_schema = True
