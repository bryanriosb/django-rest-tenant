from datetime import datetime
from django.contrib.sessions.models import Session
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.views import APIView
from rest_framework import generics
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authtoken.models import Token
from ..models import User
from .serializers import (
    UserSerializer, UserListSerializer, UserTokenSerializer, RequestPasswordResetSerializer, SetNewPasswordSerializer
)


# Verificación de email
from .utils import Util
from django.urls import reverse
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_text, smart_str, smart_bytes, DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from .utils import token_generator


@api_view(['GET', 'POST'])
def user_api_view(request):
    if request.method == 'GET':
        # queryset
        users = User.objects.all().values('id', 'username', 'email', 'password', 'name')
        users_serializer = UserListSerializer(users, many=True)
        return Response(users_serializer.data, status=status.HTTP_200_OK)

    # Registro de Usuario
    elif request.method == 'POST':
        user_serializer = UserSerializer(data=request.data)

        if user_serializer.is_valid():
            validated_data = user_serializer.validated_data
            user = User(**validated_data)
            user.is_active = False
            user.set_password(validated_data['password'])
            user.save()

            current_site = get_current_site(request)
            uid64 = urlsafe_base64_encode(force_bytes(user.pk))
            relative_link = reverse('email-verify', kwargs={'uid64': uid64, 'token': token_generator.make_token(user)})
            abs_url = f'http://{current_site}{relative_link}'

            username = validated_data['username']
            data = {
                'from': 'no-reply@gmail.com',
                'to': [validated_data['email']],
                'subject': 'Activación de cuenta',
                'body': f'Hola! {username} es necesario que pulses el siguiente enlace {abs_url} para activar la cuenta'
            }
            Util.send_email(data)

            return Response({'message': 'Usuario creado correctamente!'}, status=status.HTTP_201_CREATED)
        return Response(user_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class VerifyEmailGenericAPIView(APIView):
    """
    Se valída el correo electrónico  y se activa la cuenta de usuarios nuevos
    """

    def get(self, request, **kwargs):
        try:
            pk = force_text(urlsafe_base64_decode(kwargs.get('uid64')))
            token = kwargs.get('token')
            user = User.objects.get(pk=pk)
        except Exception as identifier:
            user = None

        if user is not None and token_generator.check_token(user, token):
            user.is_active = True
            user.save()
            return Response({'message': 'Activación de cuenta exitosa!'}, status=status.HTTP_200_OK)

        # En caso tal que ya haya expirado el enlace se elimina el usuario inactivo de la base de datos
        if user.is_active is False:
            user.delete()
        return Response({'error': 'Enlace expiró o ha ya ha sido verificado'}, status=status.HTTP_401_UNAUTHORIZED)


@api_view(['GET', 'PUT', 'DELETE'])
def user_detail_api_view(request, pk=None):
    user = User.objects.filter(id=pk).first()

    if user:
        if request.method == 'GET':
            user_serializer = UserSerializer(user)
            return Response(user_serializer.data, status=status.HTTP_200_OK)

        elif request.method == 'PUT':
            user_serializer = UserSerializer(user, data=request.data)
            if user_serializer.is_valid():
                user_serializer.save()
                return Response(user_serializer.data, status=status.HTTP_200_OK)
            return Response(user_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        elif request.method == 'DELETE':
            user.delete()
            return Response({'message': 'Usuario eliminado correctamente!'}, status=status.HTTP_200_OK)
    return Response({'message': 'No se ha encontrado un usuario con estos datos'}, status=status.HTTP_400_BAD_REQUEST)


class LoginAPIView(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        login_serializer = self.serializer_class(data=request.data, context={'request': request})

        if login_serializer.is_valid():
            user = login_serializer.validated_data['user']
            if user.is_active:
                """
                Se define la opción de crear el token en caso de no estaro
                o en su defecto obtenerlo. 
                'created' retorna True o False.
                """
                token, created = Token.objects.get_or_create(user=user)
                user_serializer = UserTokenSerializer(user)
                if created:
                    return Response(
                        {
                            'token': token.key,
                            'user': user_serializer.data,
                            'message': 'Bienvenido {}'.format(user_serializer.data['username'])
                        },
                        status=status.HTTP_201_CREATED
                    )
                else:
                    """
                    Esto para el caso que necesitemos borrar las sesiones y el token
                    cuando intentan ingresar con el mismo usuario desde diferentes 
                    lugares
                    """
                    # all_sessions = Session.objects.filter(expire_date__gte=datetime.now())
                    # if all_sessions.exists():
                    #     for session in all_sessions:
                    #         session_data = session.get_decoded()
                    #         if user.id == int(session_data.get('_auth_user_id')):
                    #             session.delete()
                    # token.delete()
                    # token = Token.objects.create(user=user)
                    # return Response({'token': token.key, 'user_data': user_serializer.data}, status=status.HTTP_200_OK)

                    """
                    Por otro lado si no se require eliminar sesión pero si bloquear 
                    el usuario 
                    """
                    token.delete()
                    return Response({'error': 'Ya hay una sesión activa para este usuario'},
                                    status=status.HTTP_409_CONFLICT)
            return Response({'error': 'Usuario no autorizado'}, status=status.HTTP_401_UNAUTHORIZED)
        return Response({'error': 'Credenciales incorrectas'}, status=status.HTTP_400_BAD_REQUEST)


class LogoutAPIView(APIView):
    def post(self, request):
        try:
            request_token = request.POST.get('token')
            token = Token.objects.filter(key=request_token).first()
            if token:
                user = token.user
                all_sessions = Session.objects.filter(expire_date__gte=datetime.now())
                if all_sessions.exists():
                    for session in all_sessions:
                        session_data = session.get_decoded()
                        if user.id == int(session_data.get('_auth_user_id')):
                            session.delete()
                token.delete()
                message = 'Sesión terminada'
                return Response({'message': message}, status=status.HTTP_200_OK)
            return Response({'error': 'Token inválido'}, status=status.HTTP_400_BAD_REQUEST)
        except Exception:
            return Response({'error': 'Falta el token'}, status=status.HTTP_400_BAD_REQUEST)


class UserTokenAPIView(APIView):
    def get(self, request, *args, **kwargs):
        username = request.GET.get('username')
        try:
            user_token = Token.objects.get(
                user=UserTokenSerializer().Meta.model.objects.filter(username=username).first()
            )
            return Response({'token': user_token.key}, status=status.HTTP_201_CREATED)
        except Exception:
            return Response({'error': 'Credenciales incorrectas'}, status=status.HTTP_400_BAD_REQUEST)


class RequestPasswordResetGenericAPIView(generics.GenericAPIView):
    serializer_class = RequestPasswordResetSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)

        email = request.data['email']

        if User.objects.filter(email=email).exists():
            user = User.objects.get(email=email)
            uid64 = urlsafe_base64_encode(smart_bytes(user.id))
            token = PasswordResetTokenGenerator().make_token(user)
            current_site = get_current_site(request=request)
            relative_link = reverse('reset-password', kwargs={'uid64': uid64, 'token': token})
            abs_url = f'http://{current_site}{relative_link}'

            email_data = {
                'from': 'admin@borls.com',
                'to': [email],
                'subject': 'Restablecer contraseña',
                'body': f'Hola! \n Use el enlace de abajo para restablecer la contraseña. \n {abs_url} '
            }
            Util.send_email(email_data)
        return Response(
            {'message': 'Hemos enviado un enlace de recuperación a su correo electrónico'},
            status=status.HTTP_200_OK
        )


class PasswordTokenCheckAPIView(APIView):
    def get(self, request, uid64, token):
        try:
            pk = smart_str(urlsafe_base64_decode(uid64))
            user = User.objects.get(id=pk)

            error_message = 'Token no es válido, por favor solicita uno nuevo'
            if not PasswordResetTokenGenerator().check_token(user, token):
                return Response({'error': error_message}, status=status.HTTP_400_BAD_REQUEST)

            return Response(
                {
                    'success': True,
                    'message': 'Credenciales válidas',
                    'uid64': uid64,
                    'token': token
                },
                status=status.HTTP_200_OK
            )
        except DjangoUnicodeDecodeError as identifier:
            return Response({'error': error_message}, status=status.HTTP_400_BAD_REQUEST)


class SetNewPasswordGenericAPIView(generics.GenericAPIView):
    serializer_class = SetNewPasswordSerializer

    def patch(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        message = 'La contraseña se restableció correctamente'
        return Response({'success': True, 'message': message}, status=status.HTTP_200_OK)
