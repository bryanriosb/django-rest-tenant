from apps.products.api.serializers.general_serializers import *
from rest_framework import viewsets


class MeasureUnitViewSet(viewsets.ModelViewSet):
    serializer_class = MeasureUnitSerializer
    queryset = MeasureUnitSerializer.Meta.model.objects.filter(state=True)


class ProductCategoryViewSet(viewsets.ModelViewSet):
    serializer_class = ProductCategorySerializer
    queryset = ProductCategorySerializer.Meta.model.objects.filter(state=True)


class IndicatorViewSet(viewsets.ModelViewSet):
    serializer_class = IndicatorSerializer
    queryset = IndicatorSerializer.Meta.model.objects.filter(state=True)
