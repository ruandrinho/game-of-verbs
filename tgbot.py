import os
import logging
from dotenv import load_dotenv
import telegram
from telegram.ext import Updater, CallbackContext, CommandHandler
from telegram.ext import MessageHandler, Filters
from google.cloud import dialogflow
from logging_utils import TelegramLogsHandler
from dialogflow_utils import get_dialogflow_reply

logger = logging.getLogger(__file__)


def start(update: telegram.Update, context: CallbackContext):
    context.bot.send_message(chat_id=update.effective_chat.id,
                             text="Привет, напиши что-нибудь")


def chat(update: telegram.Update, context: CallbackContext):
    project_id = os.getenv('GOOGLECLOUD_PROJECT_ID')
    session_id = update.effective_chat.id
    session_client = dialogflow.SessionsClient()
    session = session_client.session_path(project_id, session_id)
    reply = get_dialogflow_reply(session, session_client, update.message.text)
    context.bot.send_message(chat_id=update.effective_chat.id, text=reply)


def main():
    load_dotenv()

    logging.basicConfig(
        level=logging.DEBUG,
        format='%(asctime)s %(levelname)s %(message)s'
    )
    logging_chat_id = os.getenv('TELEGRAM_LOGGING_CHAT_ID')
    logging_bot = telegram.Bot(token=os.getenv('TELEGRAM_BOT_TOKEN'))
    logger.addHandler(TelegramLogsHandler(logging_bot, logging_chat_id))

    updater = Updater(os.getenv('TELEGRAM_BOT_TOKEN'), use_context=True)
    dispatcher = updater.dispatcher

    start_handler = CommandHandler('start', start)
    dispatcher.add_handler(start_handler)

    chat_handler = MessageHandler(Filters.text & (~Filters.command), chat)
    dispatcher.add_handler(chat_handler)

    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
