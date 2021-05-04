from rest_framework import serializers
from rest_framework.exceptions import AuthenticationFailed

from ..models import User

from django.utils.encoding import force_bytes, force_text, smart_str, smart_bytes, DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib.auth.tokens import PasswordResetTokenGenerator


class UserTokenSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'email', 'name', 'last_name')


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'

    def update(self, instance, validated_data):
        updated_user = super().update(instance, validated_data)
        updated_user.set_password(validated_data['password'])
        updated_user.save()
        return updated_user


class UserListSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'

    def to_representation(self, instance):
        return {
            'id': instance['id'],
            'username': instance['username'],
            'email': instance['email'],
            'password': instance['password']
        }


class RequestPasswordResetSerializer(serializers.Serializer):
    email = serializers.EmailField(min_length=2)

    class Meta:
        field = ['email']


class SetNewPasswordSerializer(serializers.Serializer):
    token = serializers.CharField(min_length=1, write_only=True)
    uid64 = serializers.CharField(min_length=1, write_only=True)
    password = serializers.CharField(min_length=6, max_length=68, write_only=True)

    class Meta:
        fields = ['token', 'uid64', 'password']

    def validate(self, attrs):
        try:
            token = attrs.get('token')
            uid64 = attrs.get('uid64')
            password = attrs.get('password')

            pk = smart_str(urlsafe_base64_decode(uid64))
            user = User.objects.get(id=pk)
            if not PasswordResetTokenGenerator().check_token(user, token):
                raise AuthenticationFailed('El enlace para restablecer la contraseña es inválido', 401)
            user.set_password(password)
            user.save()
        except Exception as e:
             raise AuthenticationFailed('El enlace para restablecer la contraseña es inválido', 401)
        return super().validate(attrs)



