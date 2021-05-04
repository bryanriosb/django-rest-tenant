from django.core.mail import send_mail
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from six import text_type


class Util:
    @staticmethod
    def send_email(data):
        return send_mail(
            data['subject'],
            data['body'],
            data['from'],
            data['to'],
            fail_silently=False,
        )


class AppTokenGenerator(PasswordResetTokenGenerator):
    def _make_hash_value(self, user, timestamp):
        return text_type(user.is_active) + text_type(user.pk) + text_type(timestamp)


token_generator = AppTokenGenerator()
