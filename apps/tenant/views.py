# Rest Framework
from django_tenants.admin import TenantAdminMixin
from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response

# Serializers
from .serializers import ClientSerializer, DomainSerializer, AccountSerializer

# Models
from .models import Domain, Account


class ClientViewSet(viewsets.ModelViewSet):
    serializer_class = ClientSerializer
    queryset = ClientSerializer.Meta.model.objects.all()
    pagination_class = None
    permission_classes = [IsAdminUser]

    def create(self, request, *args, **kwargs):
        tenant_data = {
            'schema_name': request.data['schema_name'],
            'name': request.data['name'],
            'paid_until': request.data['paid_until'],
            'on_trial': request.data['on_trial'],
        }
        tenant_serializer = self.serializer_class(data=tenant_data)
        tenant_serializer.is_valid(raise_exception=True)

        try:
            tenant = tenant_serializer.save()

            domain = Domain(
                domain=request.data['domain'],
                tenant=tenant,
                is_primary=True,
            )

            domain.save()

            # Set Tenant and Domain in Account
            account = Account(
                tenant=tenant,
                domain=domain,
                city=request.data['city'],
                department=request.data['department'],
                available=False
            )

            account.save()

            return Response(
                {'success': True,
                 'tenant': tenant_serializer.data
                 },
                status=status.HTTP_200_OK
            )

        except Exception as e:
            return Response(
                {
                    'success': False,
                    'error': str(e)
                },
                status=status.HTTP_400_BAD_REQUEST
            )


class DomainViewSet(viewsets.ModelViewSet):
    serializer_class = DomainSerializer
    queryset = DomainSerializer.Meta.model.objects.all()
    pagination_class = None
    permission_classes = [IsAdminUser]


class AccountViewSet(viewsets.ModelViewSet):
    serializer_class = AccountSerializer
    pagination_class = None
    permission_classes = [IsAdminUser]

    def get_queryset(self, pk=None):
        try:
            schema = self.request.GET.get('schema')
            if schema is None:
                return self.get_serializer().Meta.model.objects.all()
            return self.get_serializer().Meta.model.objects.filter(tenant__schema_name=schema)

        except Exception as e:
            return Response(
                {
                    'success': False,
                    'error': str(e)
                },
                status=status.HTTP_400_BAD_REQUEST
            )

    def partial_update(self, request, pk=None, *args, **kwargs):
        try:
            account = Account.objects.get(pk=pk)

            serializer = self.serializer_class(account, data=request.data, partial=True)
            serializer.is_valid(raise_exception=True)
            serializer.save()

            return Response(
                {
                    'success': True,
                    'account': serializer.data
                },
                status=status.HTTP_200_OK
            )

        except Exception as e:
            return Response(
                {
                    'success': False,
                    'error': str(e)
                },
                status=status.HTTP_400_BAD_REQUEST
            )
