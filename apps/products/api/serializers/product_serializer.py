from apps.products.models import Product
from rest_framework import serializers
from .general_serializers import MeasureUnitSerializer, ProductCategorySerializer


class ProductSerializer(serializers.ModelSerializer):
    # Método 1 para representar la descripción no el 'id' para las llaves Foraneas
    # product_category = serializers.StringRelatedField()
    # measure_unit = serializers.StringRelatedField()

    class Meta:
        model = Product
        exclude = ('state', 'created_date', 'modified_date', 'deleted_date',)

    def to_representation(self, instance):
        """
            Metodo 2 - Este método es el que elegimos ya que nos permite validar el valor de la imagen
            Evitando que retorne un valor null el cual genera un error a intentar instanciar
            la ruta de la imagen
        """
        return {
            'id': instance.id,
            'name': instance.name,
            'description': instance.description,
            'image': instance.image if instance.image != '' else '',
            'measure_unit': instance.measure_unit.description if instance.measure_unit is not None else '',
            'product_category': instance.product_category.description if instance.product_category is not None else ''
        }
