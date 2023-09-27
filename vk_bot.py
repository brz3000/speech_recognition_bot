import os
import random
import telegram
import vk_api as vk
from vk_api.longpoll import VkLongPoll, VkEventType
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


def message_reply(event, vk_api, project_id):
    dialogflow_answer = detect_intent_texts(project_id,
                                              event.user_id,
                                              event.text,
                                              language_code="ru")
    if dialogflow_answer[0] != "input.unknown":
        vk_api.messages.send(
            user_id=event.user_id,
            message=dialogflow_answer[1],
            random_id=random.randint(1, 1000)
        )


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
        except Exception as err:
            logger.error("Бот оповещений упал с ошибкой:")
            logger.error(err, exc_info=True)
            sleep(50)


if __name__ == '__main__':
    main()
