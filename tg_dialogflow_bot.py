import os
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from dotenv import load_dotenv
from google.cloud import dialogflow_v2beta1 as dialogflow



def start(update, context):
    first_mame = update.message.from_user.first_name
    last_name = update.message.from_user.last_name
    context.bot.send_message(chat_id=update.effective_chat.id, text=f"Здравствуйте, {first_mame} {last_name}!")


def reply(update, context):
    project_id = os.environ['GOOGLE_PROJECT_ID']
    context.bot.send_message(chat_id=update.effective_chat.id,
                             text=detect_intent_texts(project_id,
                                                      update.effective_chat.id,
                                                      update.message.text))

def detect_intent_texts(project_id, session_id, text, language_code = "ru"):
    session_client = dialogflow.SessionsClient()
    session = session_client.session_path(project_id, session_id)
    text_input = dialogflow.TextInput(text=text, language_code=language_code)
    query_input = dialogflow.QueryInput(text=text_input)
    response = session_client.detect_intent(
        request={"session": session, "query_input": query_input}
    )
    return response.query_result.fulfillment_text


def main():
    load_dotenv()
    TOKEN = os.environ['TLG_BOT']

    updater = Updater(token=TOKEN, use_context=True)
    dispatcher = updater.dispatcher

    start_handler = CommandHandler("start", start)
    dispatcher.add_handler(start_handler)
    dispatcher.add_handler(MessageHandler(Filters.text, reply))
    updater.start_polling()


if __name__ == '__main__':
    main()