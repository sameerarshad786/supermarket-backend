from django.db import models
from django.contrib.auth import get_user_model

from utils.mixins import UUID


class BotMessage(UUID):
    class MessageBy(models.TextChoices):
        BOT = "bot"
        USER = "user"

    by = models.CharField(max_length=4, choices=MessageBy.choices)
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    message = models.TextField()

    def get_message(self):
        return f"{self.message[:50]}..."
