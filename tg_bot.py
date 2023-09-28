import os
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import telegram
from dotenv import load_dotenv
from time import sleep
import logging
from detect_itent import detect_intent_texts


logger = logging.getLogger('new_logger')


class TelegramLogsHandler(logging.Handler):

    def __init__(self, tg_bot, chat_id):
        super().__init__()
        self.chat_id = chat_id
        self.tg_bot = tg_bot

    def emit(self, record):
        log_entry = self.format(record)
        self.tg_bot.send_message(chat_id=self.chat_id, text=log_entry)


def start(update, context):
    first_mame = update.message.from_user.first_name
    last_name = update.message.from_user.last_name
    context.bot.send_message(chat_id=update.effective_chat.id,
                             text=f"Здравствуйте, {first_mame} {last_name}!")


def reply(update, context):
    project_id = os.environ['GOOGLE_PROJECT_ID']
    context.bot.send_message(chat_id=update.effective_chat.id,
                             text=detect_intent_texts(project_id,
                                                      update.effective_chat.id,
                                                      update.message.text)[1])


def main():
    load_dotenv()
    token = os.environ['TLG_BOT']
    chat_id = os.environ['TLG_CHAT_ID']
    bot_logger = telegram.Bot(token=os.environ['TLG_TOKEN_LOGGER_BOT'])
    logger.setLevel(logging.DEBUG)
    logger.addHandler(TelegramLogsHandler(bot_logger, chat_id))
    logger.info('Бот оповещений запущен')
    updater = Updater(token=token, use_context=True)
    dispatcher = updater.dispatcher
    start_handler = CommandHandler("start", start)
    dispatcher.add_handler(start_handler)
    dispatcher.add_handler(MessageHandler(Filters.text, reply))
    while True:
        try:
            updater.start_polling()
        except Exception as err:
            logger.error("Бот оповещений упал с ошибкой:")
            logger.error(err, exc_info=True)
            sleep(50)


if __name__ == '__main__':
    main()
