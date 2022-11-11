from rest_framework import serializers
from .models import Client, Domain, Account


class ClientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Client
        fields = '__all__'


class DomainSerializer(serializers.ModelSerializer):
    class Meta:
        model = Domain
        fields = '__all__'

    def to_representation(self, instance):
        return {
            'id': instance.id,
            'tenant_id': instance.tenant_id,
            'domain': instance.domain,
            'is_primary': instance.is_primary          
        }


class AccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = '__all__'

    def to_representation(self, instance):
        return {
            'id': instance.id,
            'nit': instance.nit,
            'tenant': {
                'schema_name': instance.tenant.schema_name,
                'name': instance.tenant.name,
                'paid_until': instance.tenant.paid_until,
                'on_trial': instance.tenant.on_trial,
                'created_on': instance.tenant.created_on,
                'is_active': instance.tenant.is_active

            },
            'city': instance.city,
            'department': instance.department,
            'tenant_host': instance.domain.domain,
            'payment_method': {
                'name': instance.payment_method.name,
                'ref': instance.payment_method.ref,
                'description': instance.payment_method.description
            } if instance.payment_method else None,
            'responsable_billing': instance.responsable_billing,
            'billing_address': instance.billing_address,
            'electronic_billing': instance.electronic_billing,
            'phone': instance.phone,
            'email': instance.email,
            'available': instance.available,
            'modified_date': instance.modified_date
        }