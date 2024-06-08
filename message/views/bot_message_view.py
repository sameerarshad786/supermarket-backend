from rest_framework import generics

from message.models import BotMessage
from message.serializers import BotMessageSerializer


class BotMessageListAPIView(generics.ListAPIView):
    serializer_class = BotMessageSerializer

    def get_queryset(self):
        return BotMessage.objects.filter(user=self.request.user)


class BotMessageCreateAPIView(generics.CreateAPIView):
    serializer_class = BotMessageSerializer
    queryset = BotMessage.objects.all()
