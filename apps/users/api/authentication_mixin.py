from rest_framework.authentication import get_authorization_header
from .authentication import ExpiringTokenAuthentication
from rest_framework.response import Response
from rest_framework.renderers import JSONRenderer
from rest_framework import status


class Authentication(object):
    user = None
    user_token_expired = False

    def get_user(self, request):
        token = get_authorization_header(request).split()
        if token:
            try:
                token_decode = token[1].decode()
            except:
                return None

            token_expire = ExpiringTokenAuthentication()
            user, token, message, self.user_token_expired = token_expire.authenticate_credentials(token_decode)

            if user is not None and token is not None:
                self.user = user
                return user
            return message
        return None

    def dispatch(self, request, *args, **kwargs):
        """
        Este método se ejecuta al inicio de una clase en DFRF
        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        user = self.get_user(request)
        if user is not None:
            """
            Validamos si user es de tipo str ya que puede retornar dos tipos de 
            datos, si lo es, se ha enviado un mensaje sino se retorna el usuario propiamente
            """
            if type(user) == str:
                response = Response(
                    {
                        'error': user,
                        'expired': self.user_token_expired
                    },
                    status=status.HTTP_401_UNAUTHORIZED
                )
                response.accepted_renderer = JSONRenderer()
                response.accepted_media_type = 'application/json'
                response.renderer_context = {}
                return response

            if not self.user_token_expired:
                return super().dispatch(request, *args, **kwargs)
        response = Response(
            {
                'error': 'No se han enviado las credenciales',
                'expired': self.user_token_expired
            },
            status=status.HTTP_400_BAD_REQUEST
        )
        response.accepted_renderer = JSONRenderer()
        response.accepted_media_type = 'application/json'
        response.renderer_context = {}
        return response
