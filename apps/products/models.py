from django.db import models
from simple_history.models import HistoricalRecords
from apps.base.models import BaseModel


class MeasureUnit(BaseModel):
    """
    Unidad de medida
    """
    description = models.CharField('Descripción', max_length=50, blank=False, null=False, unique=True)
    historical = HistoricalRecords()

    # Son proiedades necesarias para permitir que se identiique el usuario que realizó los cambios
    @property
    def _history_user(self):
        return self.changed_by

    @_history_user.setter
    def _history_user(self, value):
        self.changed_by = value

    class Meta:
        verbose_name = 'Unidad de medida'
        verbose_name_plural = 'Unidades de medida'

    def __str__(self):
        return self.description


class ProductCategory(BaseModel):
    description = models.CharField('Descripción', max_length=50, blank=False, null=False, unique=True)
    historical = HistoricalRecords()

    @property
    def _history_user(self):
        return self.changed_by

    @_history_user.setter
    def _history_user(self, value):
        self.changed_by = value

    def __str__(self):
        return self.description

    class Meta:
        verbose_name = 'Categoría'
        verbose_name_plural = 'Categorías'


class Product(BaseModel):
    name = models.CharField('Nombre de producto', max_length=150, unique=True, blank=False, null=False)
    description = models.TextField('Descripción', unique=True, blank=False, null=False)
    image = models.ImageField('Imagen de producto', upload_to='products/', blank=True, null=True)
    measure_unit = models.ForeignKey(MeasureUnit, on_delete=models.CASCADE, verbose_name='Unidad de medida', null=True)
    product_category = models.ForeignKey(ProductCategory, on_delete=models.CASCADE, verbose_name='Categoría', null=True)
    historical = HistoricalRecords()

    @property
    def _history_user(self):
        return self.changed_by

    @_history_user.setter
    def _history_user(self, value):
        self.changed_by = value

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Producto'
        verbose_name_plural = 'Productos'


class Indicator(BaseModel):
    off_value = models.PositiveSmallIntegerField(default=0)
    product_category = models.ForeignKey(ProductCategory, on_delete=models.CASCADE, verbose_name='Categoría de Producto')
    historical = HistoricalRecords()

    @property
    def _history_user(self):
        return self.changed_by

    @_history_user.setter
    def _history_user(self, value):
        self.changed_by = value

    def __str__(self):
        return f'Oferta de la categoría {self.product_category} : {self.off_value}%'

    class Meta:
        verbose_name = 'Indicador de oferta'
        verbose_name_plural = 'Indicadores de oferta'


