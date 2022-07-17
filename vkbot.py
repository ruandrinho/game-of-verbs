import os
import logging
from dotenv import load_dotenv
import random
import telegram
import vk_api
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType
from google.cloud import dialogflow
from logging_utils import TelegramLogsHandler
from dialogflow_utils import get_dialogflow_reply

logger = logging.getLogger(__file__)


def reply_to_message(event, vk_api, project_id):
    project_id = os.getenv('GOOGLECLOUD_PROJECT_ID')
    session_id = event.obj['message']['from_id']
    session_client = dialogflow.SessionsClient()
    session = session_client.session_path(project_id, session_id)
    reply = get_dialogflow_reply(session, session_client,
                                 event.obj['message']['text'])
    if reply:
        vk_api.messages.send(
            user_id=session_id,
            message=reply,
            random_id=random.randint(1, 1000)
        )


def main():
    load_dotenv()

    logging.basicConfig(
        level=logging.DEBUG,
        format='%(asctime)s %(levelname)s %(message)s'
    )
    logging_chat_id = os.getenv('TELEGRAM_LOGGING_CHAT_ID')
    logging_bot = telegram.Bot(token=os.getenv('TELEGRAM_BOT_TOKEN'))
    logger.addHandler(TelegramLogsHandler(logging_bot, logging_chat_id))

    vk_session = vk_api.VkApi(token=os.getenv('VK_BOT_TOKEN'))
    vk_session_api = vk_session.get_api()
    longpoll = VkBotLongPoll(vk_session, os.getenv('VK_BOT_GROUP_ID'))

    project_id = os.getenv('GOOGLECLOUD_PROJECT_ID')
    for event in longpoll.listen():
        if event.type == VkBotEventType.MESSAGE_NEW:
            reply_to_message(event, vk_session_api, project_id)


if __name__ == '__main__':
    main()
