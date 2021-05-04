from apps.products.models import MeasureUnit, ProductCategory, Indicator
from rest_framework import serializers


class MeasureUnitSerializer(serializers.ModelSerializer):
    class Meta:
        model = MeasureUnit
        exclude = ('state', 'created_date', 'modified_date', 'deleted_date',)


class ProductCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductCategory
        exclude = ('state', 'created_date', 'modified_date', 'deleted_date',)


class IndicatorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Indicator
        exclude = ('state', 'created_date', 'modified_date', 'deleted_date',)
