from rest_framework.generics import ListAPIView


class GeneralListAPIView(ListAPIView):
    """
        Nos permite generalizar al momento de realizar un  get query para la vista ListAPIView
        lo cual dara lugar a la oportunidad de heredar por parte de la vista
        evitando así escribir varias veces el método get_queryset
    """
    serializer_class = None

    def get_queryset(self):
        model = self.get_serializer().Meta.model
        return model.objects.filter(state=True)
