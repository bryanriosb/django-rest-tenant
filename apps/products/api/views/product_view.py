from ..serializers.product_serializer import ProductSerializer
from rest_framework import status, viewsets
from rest_framework.response import Response
from apps.users.api.authentication_mixin import Authentication


class ProductViewSet(Authentication, viewsets.ModelViewSet):
    serializer_class = ProductSerializer
    queryset = ProductSerializer.Meta.model.objects.filter(state=True)

    def get_queryset(self, pk=None):
        if pk is None:
            return self.get_serializer().Meta.model.objects.filter(state=True)
        return self.get_serializer().Meta.model.objects.filter(id=pk, state=True).first()

    def create(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'Producto creado correctamente'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, pk=None, **kwargs):
        product = self.get_queryset(pk)
        if product:
            product_serializer = self.serializer_class(product, data=request.data)
            if product_serializer.is_valid():
                product_serializer.save()
                return Response(product_serializer.data, status=status.HTTP_200_OK)
            return Response(product_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk=None, **kwargs):
        """
        En este caso eliminamos de forma lógica,  no eliminación
        directa de la base de datos
        :param request:
        :param pk:
        :param kwargs:
        :return:
        """
        product = self.get_queryset().filter(id=pk).first()

        if product:
            product.state = False
            product.save()
            return Response({'Mensaje': 'Producto eliminado correctamente'}, status=status.HTTP_200_OK)
        return Response({'Error': 'No existe un producto con estos datos'}, status=status.HTTP_400_BAD_REQUEST)