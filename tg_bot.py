import os
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from dotenv import load_dotenv
from detect_itent import detect_intent_texts


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
                                                      update.message.text))


def main():
    load_dotenv()
    token = os.environ['TLG_BOT']
    updater = Updater(token=token, use_context=True)
    dispatcher = updater.dispatcher

    start_handler = CommandHandler("start", start)
    dispatcher.add_handler(start_handler)
    dispatcher.add_handler(MessageHandler(Filters.text, reply))
    updater.start_polling()


if __name__ == '__main__':
    main()
