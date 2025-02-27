import os
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from chat.routing import websocket_urlpatterns
import django
from channels.auth import AuthMiddlewareStack



os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'SoccerPedia.settings')
application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket": URLRouter(websocket_urlpatterns),
})
