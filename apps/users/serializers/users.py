# Django
from abc import ABC

from django.conf import settings
from django.contrib.auth import authenticate
from django.utils.encoding import smart_str
from django.utils.http import urlsafe_base64_decode
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.contrib.auth.models import User

# Django REST Framework
from rest_framework import serializers
from rest_framework.authtoken.models import Token
from rest_framework.exceptions import AuthenticationFailed

# Models
from apps.users.models import Profile

# Utils
import os
import jwt


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        """Meta class."""
        model = User
        fields = '__all__'
    
    def to_representation(self, instance):
        return {
            'id': instance.id,
            'username': instance.username,
            'first_name': instance.first_name,
            'last_name': instance.last_name,
            'email': instance.email,
            'role': instance.profile.role   
        }


class UserSignInSerializer(serializers.Serializer):
    """User login serializer.
    Handle the login request data.
    """
    username = serializers.CharField()
    password = serializers.CharField(min_length=8, max_length=64)

    def validate(self, data):
        """Check credentials."""
        user = authenticate(username=data['username'], password=data['password'])

        if not user:
            raise serializers.ValidationError('Credenciales inválidas!')
        if not user.is_active:
            raise serializers.ValidationError('La cuenta no está activa :(')
        self.context['user'] = user
        return data

    def create(self, data):
        """Generate or retrieve new token."""
        token, created = Token.objects.get_or_create(user=self.context['user'])
        return self.context['user'], token.key


class UserSignOutSerializer(serializers.Serializer):
    token = serializers.CharField()


class VerificationEmailSerializer(serializers.Serializer):
    """Verificación de cuenta serializer."""
    token = serializers.CharField()

    def validate_token(self, data):
        """comprobar la validez del token."""
        try:
            payload = jwt.decode(data, os.environ.get('JWT_SECRET_KEY'), algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            raise serializers.ValidationError('La verificación ha expirado')
        except jwt.PyJWTError as e:
            raise serializers.ValidationError('Token inválido')
        if payload['type'] != 'email_confirmation':
            raise serializers.ValidationError('Token de tipo incorrecto')

        self.context['payload'] = payload
        return data

    def save(self):
        """Actualiación del estado de disponibilidad del usuario."""
        payload = self.context['payload']
        user = User.objects.get(username=payload['data']['username'])
        
        if user.is_active:
            raise serializers.ValidationError('El usuario ya está verificado')
            
        user.is_active = True
        user.save()


class RefreshTokenSerializer(serializers.Serializer):
    payload = serializers.CharField()


class RequestPasswordResetSerializer(serializers.Serializer):
    email = serializers.EmailField()


class SetNewPasswordSerializer(serializers.Serializer):
    token = serializers.CharField()
    password = serializers.CharField()
    user_id = serializers.IntegerField()

    def validate(self, attrs):
        try: 
            token = attrs.get('token')
            password = attrs.get('password')
            user_id = attrs.get('user_id')
            
            user = User.objects.get(id=user_id)

            if not PasswordResetTokenGenerator().check_token(user, token):
                raise AuthenticationFailed('El enlace para restablecer la contraseña es inválido', 401)
            
            self.context['user'] = user
            self.context['password'] = password
        except Exception as e:
            raise AuthenticationFailed('El enlace para restablecer la contraseña es inválido', 401)

        return super().validate(attrs)

    def save(self):
        user = self.context['user']
        password = self.context['password']
        user.set_password(password)
        user.save()