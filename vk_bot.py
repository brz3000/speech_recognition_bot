import os
import random
import telegram
import vk_api as vk
from vk_api.longpoll import VkLongPoll, VkEventType
from dotenv import load_dotenv
from google.cloud import dialogflow_v2beta1 as dialogflow
from time import sleep
import logging


logger = logging.getLogger('new_logger')


class TelegramLogsHandler(logging.Handler):

    def __init__(self, tg_bot, chat_id):
        super().__init__()
        self.chat_id = chat_id
        self.tg_bot = tg_bot

    def emit(self, record):
        log_entry = self.format(record)
        self.tg_bot.send_message(chat_id=self.chat_id, text=log_entry)



def detect_intent_texts(project_id, session_id, texts, language_code="ru"):
    session_client = dialogflow.SessionsClient()
    session = session_client.session_path(project_id, session_id)
    text_input = dialogflow.TextInput(text=texts, language_code=language_code)
    query_input = dialogflow.QueryInput(text=text_input)
    response = session_client.detect_intent(
        request={"session": session, "query_input": query_input}
    )
    if response.query_result.intent.is_fallback:
        return False
    else:
        return response.query_result.fulfillment_text


def message_reply(event, vk_api, project_id):
    is_fallback = detect_intent_texts(project_id,
                                      event.user_id,
                                      event.text,
                                      language_code="ru")
    if is_fallback:
        vk_api.messages.send(
            user_id=event.user_id,
            message=is_fallback,
            random_id=random.randint(1, 1000)
        )
    else:
        pass


def main():
    load_dotenv()
    chat_id = os.environ['TLG_CHAT_ID']
    bot_logger = telegram.Bot(token=os.environ['TLG_TOKEN_LOGGER_BOT'])
    logger.setLevel(logging.DEBUG)
    logger.addHandler(TelegramLogsHandler(bot_logger, chat_id))
    logger.info('Бот оповещений запущен')
    project_id = os.environ['GOOGLE_PROJECT_ID']
    vk_session = vk.VkApi(token=os.environ['VK_GROUP_ACCESS_TOKEN'])
    vk_api = vk_session.get_api()
    longpoll = VkLongPoll(vk_session)
    while True:
        try:
            for event in longpoll.listen():
                if event.type == VkEventType.MESSAGE_NEW and event.to_me:
                    message_reply(event, vk_api, project_id)
        except requests.exceptions.ConnectionError:
            sleep(5)
        except requests.exceptions.ReadTimeout:
            pass
        except Exception as err:
            logger.error("Бот оповещений упал с ошибкой:")
            logger.error(err, exc_info=True)
            sleep(50)


if __name__ == '__main__':
    main()
