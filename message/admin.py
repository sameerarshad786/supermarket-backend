from django.contrib import admin

from message import models


@admin.register(models.BotMessage)
class BotMessageAdmin(admin.ModelAdmin):
    list_display = ("id", "by", "user", "get_message")
