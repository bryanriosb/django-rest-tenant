import os
import sys

import django
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "manager.config.dev")

django.setup()

django_app = get_asgi_application()

application = ProtocolTypeRouter({
    'http': django_app,
    # 'websocket': AuthMiddlewareStack(
    #     URLRouter(
    #         apps.meet.routing.websocket_urlpatterns
    #     )
    # )
})
