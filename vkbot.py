import os
import logging
from dotenv import load_dotenv
import vk_api
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType
from google.cloud import dialogflow


def get_dialogflow_reply(session, session_client, text, language_code='ru-RU'):
    text_input = dialogflow.TextInput(text=text,
                                      language_code=language_code)
    query_input = dialogflow.QueryInput(text=text_input)
    response = session_client.detect_intent(
        request={'session': session, 'query_input': query_input}
    )
    return response.query_result.fulfillment_text


def main():
    load_dotenv()

    logging.basicConfig(
        level=logging.DEBUG,
        format='%(asctime)s %(levelname)s %(message)s'
    )
    # logger.addHandler(TelegramLogsHandler(bot, chat_id))

    vk_session = vk_api.VkApi(token=os.getenv('VK_BOT_TOKEN'))
    longpoll = VkBotLongPoll(vk_session, '214464975')

    for event in longpoll.listen():
        if event.type == VkBotEventType.MESSAGE_NEW:
            print('Новое сообщение:')
            print('Для меня от:', event.obj['message']['from_id'])
            print('Текст:', event.obj['message']['text'])
            print()


if __name__ == '__main__':
    main()
