import os
import logging
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import Updater, CallbackContext, CommandHandler
from telegram.ext import MessageHandler, Filters


def start(update: Update, context: CallbackContext):
    context.bot.send_message(chat_id=update.effective_chat.id,
                             text="Здравствуйте")


def echo(update: Update, context: CallbackContext):
    context.bot.send_message(chat_id=update.effective_chat.id,
                             text=update.message.text)


def main():
    load_dotenv()

    logging.basicConfig(
        level=logging.DEBUG,
        format='%(asctime)s %(levelname)s %(message)s'
    )
    # logger.addHandler(TelegramLogsHandler(bot, chat_id))

    updater = Updater(os.getenv('TELEGRAM_BOT_TOKEN'), use_context=True)
    dispatcher = updater.dispatcher
    start_handler = CommandHandler('start', start)
    dispatcher.add_handler(start_handler)
    echo_handler = MessageHandler(Filters.text & (~Filters.command), echo)
    dispatcher.add_handler(echo_handler)
    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
