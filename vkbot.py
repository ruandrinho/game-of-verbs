import os
import logging
from dotenv import load_dotenv
import random
import telegram
import vk_api
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType
from google.cloud import dialogflow

logger = logging.getLogger(__file__)


class TelegramLogsHandler(logging.Handler):

    def __init__(self, tg_bot, chat_id):
        super().__init__()
        self.chat_id = chat_id
        self.tg_bot = tg_bot

    def emit(self, record):
        log_entry = self.format(record)
        self.tg_bot.send_message(chat_id=self.chat_id, text=log_entry)


def chat(event, vk_api):
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


def get_dialogflow_reply(session, session_client, text, language_code='ru-RU'):
    text_input = dialogflow.TextInput(text=text,
                                      language_code=language_code)
    query_input = dialogflow.QueryInput(text=text_input)
    response = session_client.detect_intent(
        request={'session': session, 'query_input': query_input}
    )
    if response.query_result.intent.is_fallback:
        return
    return response.query_result.fulfillment_text


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

    for event in longpoll.listen():
        if event.type == VkBotEventType.MESSAGE_NEW:
            chat(event, vk_session_api)


if __name__ == '__main__':
    main()
