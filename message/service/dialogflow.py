import os
import uuid
import json
import dialogflow_v2 as dialogflow

from django.core.serializers.json import DjangoJSONEncoder

from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync

from message.models import BotMessage


def send_and_recieve_message_from_bot(request):
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "credentials/google.json"
    session_client = dialogflow.SessionsClient()
    language_code = "en-US"
    session_id = uuid.uuid4()
    project_id = "newagent-qscn"
    session = session_client.session_path(project_id, session_id)
    text_input = dialogflow.types.TextInput(
        text=f"hi {request.user.profile.full_name}",
        language_code=language_code
    )
    query_input = dialogflow.types.QueryInput(text=text_input)
    response = session_client.detect_intent(
        session=session,
        query_input=query_input
    )
    channel_layer = get_channel_layer()
    group_name = str(f"supermarket-bot-{request.user.id}")
    bot_response = response.query_result.fulfillment_text
    instance = BotMessage.objects.create(
        user=request.user,
        by=BotMessage.MessageBy.BOT,
        message=bot_response
    )
    from message.serializers import BotMessageSerializer
    serializer = BotMessageSerializer(
        instance,
        context={"request": request}
    )

    async_to_sync(channel_layer.group_send)(
        group_name, {
            "type": "chat.message",
            "action": "CREATED",
            "data": json.dumps(
                serializer.data,
                cls=DjangoJSONEncoder
            )
        }
    )
    return serializer.data
