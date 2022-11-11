# Utils
import os
import jwt
from datetime import date, timedelta

# Django
from django.urls import reverse
from django.contrib.sessions.models import Session
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.template.loader import render_to_string
from django.urls.base import reverse_lazy
from django.utils import timezone
from django.contrib.auth.models import User

# Rest Framework
from rest_framework.views import APIView
from rest_framework import mixins, status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken

# Apps
from apps.common.utils import send_email
from apps.common.utils import gen_jwt
from ..utils import token_generator
from ..models import Profile

from ..serializers.users import (
    UserSerializer,
    UserSignInSerializer,
    VerificationEmailSerializer,
    UserSignOutSerializer,
    RequestPasswordResetSerializer,
    RefreshTokenSerializer,
    SetNewPasswordSerializer
)


class UserViewSet(viewsets.ModelViewSet):
    """User ModelViewSet."""
    serializer_class = UserSerializer

    def get_queryset(self, pk=None):
        user_id = self.request.GET.get('user_id')

        if user_id is None:
            return self.get_serializer().Meta.model.objects.all()
        return self.get_serializer().Meta.model.objects.filter(id=user_id)
    
    def create(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        try:
            user = self.get_serializer().Meta.model(** serializer.validated_data)
            # user.is_active = False
            user.is_active = True
            user.set_password(request.data['password'])

            user.save()
            profile = Profile.objects.create(user=user, role=request.data['role'])
            user_result = profile.save()

            user_data = self.serializer_class(user)

            return Response(
                {
                    'success': True,
                    'user': user_data.data
                }, status=status.HTTP_201_CREATED
            )

            # email_sent  = self.send_confirmation_email(request, user)

            # if email_sent:
            #     user.save()
            #     profile = Profile.objects.create(user=user, role=request.data['role'])
            #     user_result = profile.save()
            #
            #     user_data = self.serializer_class(user)
            #     return Response(
            #         {
            #             'success': True,
            #             'user': user_data.data
            #         }, status=status.HTTP_201_CREATED
            #     )
            # else:
            #     return Response(
            #         {
            #             'success': False,
            #             'error': 'Hubo problemas con el envio del correo, intenta de nuevo.'
            #         }, status=status.HTTP_400_BAD_REQUEST
            #     )
            
        except Exception as e:
            return Response(
                {   
                    'success': False,
                    'error': f'No se pudo crear el usuario por {e}'
                }, status=status.HTTP_400_BAD_REQUEST
            )

    @staticmethod
    def send_confirmation_email(request, user):
        """Envío del correo electrónico de activación."""

        try:
            token = gen_jwt({'username': user.username}, 'email_confirmation', True)
            client_host = os.getenv('CLIENT_HOST')
            abs_url = f'{client_host}/email-verification/{request.tenant.schema_name}/{token}'

            now_time = date.today()
            date_email = now_time.strftime("%d/%m/%Y")
            exp_date = now_time + timedelta(days=3)

            email_context = {
                'abs_url': abs_url,
                'body': f'Hola! {user} es necesario que pulses el siguiente botón para activar la cuenta.',
                'date': date_email,
                'exp_date': exp_date.strftime("%d/%m/%Y")
            }

            msg_html = render_to_string('mails/account-verify.html', email_context)

            email_data = {
                'from': 'BORLS <noreply@niimx.io>',
                'to': [user.email],
                'subject': 'NiiMX - Account Activate',
                'html': msg_html,
            }
            send_email(email_data)

            return True
        except Exception as e:
            print(f'Error al enviar correo por {e}')
            return False


class VerificationEmailViewSet(viewsets.ViewSet):
    """Verificación de email ModelViewSet."""
    serializer_class = VerificationEmailSerializer

    def create(self, request, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(
            {   
                'success': True,
                'message': 'Activación de cuenta exitosa!'
            }, status=status.HTTP_200_OK
        )
        
        
class SignInViewSet(viewsets.GenericViewSet):
    """User login ModelViewSet."""
    serializer_class = UserSignInSerializer
    queryset = User.objects.filter(is_active=True)

    def create(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        user, token = serializer.save()

        data = {
            'id': user.id,
            'username': user.username,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'is_active': user.is_active,
            'role': user.profile.role  
        }

        return Response(
            {   
                'success': True,
                'user': data,
                'access_token': token
            }, status=status.HTTP_201_CREATED
        )
    

class SignOutViewSet(viewsets.ViewSet):
    """User logout ModelViewSet."""
    serializer_class = UserSignOutSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        request_token = request.data['token']
        token = Token.objects.filter(key=request_token).first()

        try:
            user = token.user
            all_sessions = Session.objects.filter(
                expire_date__gte=timezone.now())
            if all_sessions.exists():
                for session in all_sessions:
                    session_data = session.get_decoded()
                    if user.id == int(session_data.get('_auth_user_id')):
                        session.delete()
            token.delete()

            return Response(
                {   
                    'success': True,
                    'message': 'Sesión terminada'
                }, status=status.HTTP_200_OK
            )
        except Exception as e:
            return Response(
                {   
                    'success': False,
                    'error': f'Token inválido por {e}'
                }, status=status.HTTP_400_BAD_REQUEST
            )


class RefreshTokenViewSet(viewsets.ViewSet):
    """Refresh User Token ModelViewSet."""
    serializer_class = RefreshTokenSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        data = jwt.decode(request.data['payload'], os.environ.get('JWT_SECRET_KEY'), algorithms=['HS256'])
        user = self.get_serializer().Meta.model.objects.get(username=data['username'])

        try:
            token, created = Token.objects.get_or_create(user=user)
            if created:
                return Response(
                    {   
                        'success': True,
                        'token': token.key
                    }, status=status.HTTP_201_CREATED
                )
            return Response(
                {   
                    'success': True,
                    'token': token.key
                }, status=status.HTTP_200_OK
            )
        except Exception as e:
            return Response(
                {   
                    'success': False,
                    'error': f'Error al crear el token por {e}'
                }, status=status.HTTP_400_BAD_REQUEST
            )


class RequestPasswordResetViewSet(viewsets.ViewSet):
    serializer_class = RequestPasswordResetSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        try:
            email = request.data['email']
            user = User.objects.get(email=email)

            if user:
                token = PasswordResetTokenGenerator().make_token(user)

                print('Debug', user.id)

                jwt_token = gen_jwt(
                    {
                        'token': token,
                        'user_id': user.id,
                    }, 'reset_password', True
                )

                client_host = os.getenv('CLIENT_HOST')
                abs_url = f'{client_host}/password-reset/{request.tenant.schema_name}/{jwt_token}'

                now_time = date.today()
                date_email = now_time.strftime("%d/%m/%Y")
                exp_date = now_time + timedelta(days=3)
        
                email_context = {
                    'abs_url': abs_url,
                    'body': f'Hola! {user}, haz click en el botón para continuar con el proceso de restauración de la contraseña.',
                    'date': date_email,
                    'exp_date': exp_date.strftime("%d/%m/%Y")
                }
                
                msg_html = render_to_string('mails/password-reset.html', email_context)

                email_data = {
                    'from': 'BORLS <noreply@borls.tech>',
                    'to': [user.email],
                    'subject': 'BORLS - Restablecer contraseña',
                    'html': msg_html,
                }
                send_email(email_data)

                return Response(
                    {
                        'success': True,
                        'message': f'Solicitud envíada al correo {user.email}'
                    }, status=status.HTTP_200_OK
                )
        except Exception as e:
            return Response(
                {   
                    'success': False,
                    'error': f'El correo ingresado es inválido'
                }, status=status.HTTP_400_BAD_REQUEST
            )


class SetNewPasswordViewSet(viewsets.ViewSet):
    serializer_class = SetNewPasswordSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        print('Debug', request.data)
        serializer.save()

        return Response(
            {   
                'success': True,
                'message': 'La contraseña se restableció correctamente'
            }, status=status.HTTP_200_OK
        )