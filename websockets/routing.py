from django.urls import path

from channels.routing import URLRouter

from . import consumers

BOT_URLS_PATTERNS = [
    path("bot-message/", consumers.BotMessageConsumer.as_asgi())
]

websocket_urlpatterns = [
    path("ws/", URLRouter(BOT_URLS_PATTERNS))
]
