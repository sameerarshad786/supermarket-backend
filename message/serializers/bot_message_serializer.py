import threading

from rest_framework import serializers

from message.models import BotMessage
from message.service import send_and_recieve_message_from_bot


class BotMessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = BotMessage
        fields = ("id", "by", "user", "message")
        extra_kwargs = {
            "user": {"read_only": True},
            "by": {"read_only": True}
        }

    def create(self, validated_data):
        request = self.context["request"]
        instance = BotMessage.objects.create(
            user=request.user,
            by=BotMessage.MessageBy.USER,
            **validated_data
        )
        task = threading.Thread(target=send_and_recieve_message_from_bot, args=(request, ))
        task.start()
        return instance
