import os
import logging
from dotenv import load_dotenv
import random
import vk_api
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType
from google.cloud import dialogflow


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
    # logger.addHandler(TelegramLogsHandler(bot, chat_id))

    vk_session = vk_api.VkApi(token=os.getenv('VK_BOT_TOKEN'))
    vk_session_api = vk_session.get_api()
    longpoll = VkBotLongPoll(vk_session, os.getenv('VK_BOT_GROUP_ID'))

    for event in longpoll.listen():
        if event.type == VkBotEventType.MESSAGE_NEW:
            chat(event, vk_session_api)


if __name__ == '__main__':
    main()