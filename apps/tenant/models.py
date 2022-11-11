from django.db import models
import uuid
from django_tenants.models import TenantMixin, DomainMixin
from apps.common.models import BaseModelNotRef


class Client(TenantMixin):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100)
    paid_until = models.DateField()
    on_trial = models.BooleanField()
    created_on = models.DateField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

    auto_create_schema = True

    class Meta:
        verbose_name = 'Client'

    def __str__(self):
        """:return name."""
        return self.name


class Domain(DomainMixin):
    pass

    class Meta:
        verbose_name = 'Domain'
    
    def __str__(self):
        """:return domain."""
        return self.domain


class PaymentMethod(BaseModelNotRef):
    name = models.CharField('Nombre', max_length=100)
    ref = models.SlugField('Ref', max_length=100, null=True)
    description = models.CharField('Descripción', max_length=255)

    class Meta:
        verbose_name = 'Método de Pago'

    def __str__(self):
        """:return name."""
        return self.name


class Account(BaseModelNotRef):
    nit = models.CharField('NIT', max_length=10, null=True, blank=True)
    tenant = models.ForeignKey(
        Client,
        verbose_name='Tenant',
        on_delete=models.CASCADE,
    )
    domain = models.ForeignKey(
        Domain,
        verbose_name='Host Tenant',
        on_delete=models.CASCADE,
    )
    payment_method = models.ForeignKey(
        PaymentMethod,
        verbose_name='Método de pago',
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )
    responsable_billing = models.CharField(
        'Responsable Facturación',
        max_length=255,
        null=True,
        blank=True
    )
    city = models.CharField('Ciudad', max_length=255, default='Cali')
    department = models.CharField('Departamento', max_length=255, default='Valle del Cauca')
    billing_address = models.CharField('Dirección Facturación', max_length=255, null=True, blank=True)
    electronic_billing = models.BooleanField('¿Factura Electrónica?', default=True)
    phone = models.CharField('Teléfono', max_length=10, null=True, blank=True)
    email = models.EmailField('Correo', null=True, blank=True)

    class Meta:
        verbose_name = 'Cuenta'

    def __str__(self):
        """:return company name."""
        return self.tenant.name

