from django.db import models
import uuid


class BaseModel(models.Model):
    """Estructura common de los modelos con Ref."""
    id = models.UUIDField('ID', primary_key=True, default=uuid.uuid4, editable=False)
    ref = models.SlugField('REF.', unique=True, max_length=100, null=False, blank=False)
    available = models.BooleanField('Disponible', default=True)
    created_date = models.DateField('Fecha de creación', auto_now=False, auto_now_add=True)
    modified_date = models.DateField('Fecha de modificación', auto_now=True, auto_now_add=False)

    class Meta:
        abstract = True
        verbose_name = 'Modelo Base Ref'


class BaseModelNotRef(models.Model):
    """Estructura common de los modelos sin ref."""
    id = models.UUIDField('ID', primary_key=True, default=uuid.uuid4, editable=False)
    available = models.BooleanField('Disponible', default=True)
    created_date = models.DateField('Fecha de creación', auto_now=False, auto_now_add=True)
    modified_date = models.DateField('Fecha de modificación', auto_now=True, auto_now_add=False)

    class Meta:
        abstract = True
        verbose_name = 'Modelo Base Not Ref'


