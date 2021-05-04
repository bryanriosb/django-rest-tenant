from datetime import timedelta
from django.utils import timezone
from rest_framework.authentication import TokenAuthentication
from rest_framework.exceptions import AuthenticationFailed
from django.conf import settings


class ExpiringTokenAuthentication(TokenAuthentication):
    """
        Esta clase hereda de la clase TokenAuthentication de DRF
        en ese orden de ideas podemos definir periodos de expiración
        para el Token
    """

    expired = False

    def expires_in(self, token):
        time_elapsed = timezone.now() - token.created
        token_expired = settings.TOKEN_EXPIRED_AFTER_SECONDS
        left_time = timedelta(seconds=token_expired) - time_elapsed
        return left_time

    def is_token_expired(self, token):
        return self.expires_in(token) < timedelta(seconds=0)

    def token_expire_handler(self, token):
        is_expire = self.is_token_expired(token)
        if is_expire:
            self.expired = False

            user = token.user
            token.delete()
            token = self.get_model().objects.create(user=user)
        return is_expire, token

    def authenticate_credentials(self, key):
        user, token, message = None, None, None
        token_model = self.get_model()

        try:
            token = token_model.objects.select_related('user').get(key=key)
            user = token.user
        except token_model.DoesNotExist:
            message = 'Token inválido'
            self.expired = True

        if token is not None:
            if not token.user.is_active:
                message = 'Usuario inactivo o eliminado'

            is_expired = self.token_expire_handler(token)
            if is_expired:
                message = 'El token ha expirado'
        return user, token, message, self.expired
