from channels.routing import ProtocolTypeRouter, URLRouter
from channels.security.websocket import AllowedHostsOriginValidator, OriginValidator
from django.urls import path
from app.consumers import RunProgram, AlwaysRunProgram

application = ProtocolTypeRouter({
    'websocket': AllowedHostsOriginValidator(
        URLRouter(
            [
                path('live-console/<id>', RunProgram),
                path('always-live-console/<id>', AlwaysRunProgram)
            ]
        )
    )
})
