import json

from channels.generic.websocket import AsyncJsonWebsocketConsumer


class BotMessageConsumer(AsyncJsonWebsocketConsumer):
    async def connect(self):
        await self.accept()
        self.user = self.scope["user"]
        self.group_name = str(f"supermarket-bot-{self.user.id}")
        await self.channel_layer.group_add(
            self.group_name, self.channel_name
        )

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.group_name, self.channel_name
        )

    async def chat_message(self, event):
        await self.send(text_data=json.dumps({
            "type": event["type"],
            "action": event["action"],
            "data": json.loads(event["data"])
        }))
