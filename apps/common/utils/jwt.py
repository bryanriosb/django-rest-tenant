# Django
from django.utils import timezone

# Utils
import os
import jwt
from datetime import timedelta


def gen_jwt(data, type: str, exp: bool, exp_days=3):
    """Crear un JWK con la data que se pasa por parámetro. """
    if exp:
        exp_date = timezone.now() + timedelta(days=exp_days)
        payload = {
            'data': data,
            'exp': int(exp_date.timestamp()),
            'type': type
        }
    else:
        payload = {
            'data': data,
            'type': type
        }

    token = jwt.encode(payload, os.environ.get('JWT_SECRET_KEY'), algorithm='HS256')
    return token
