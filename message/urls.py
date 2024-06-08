from django.urls import path, include

from message import views


BOT_MESSAGE_PATTERS = [
    path(
        "list/",
        views.BotMessageListAPIView.as_view(),
        name="bot-message-list"
    ),
    path(
        "create/",
        views.BotMessageCreateAPIView.as_view(),
        name="bot-message-create"
    )
]


urlpatterns = [
    path("bot-messages/", include(BOT_MESSAGE_PATTERS))
]
