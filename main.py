import os
import random
import vk_api as vk
from vk_api.longpoll import VkLongPoll, VkEventType
from dotenv import load_dotenv
from google.cloud import dialogflow_v2beta1 as dialogflow
from time import sleep


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
    project_id = os.environ['GOOGLE_PROJECT_ID']
    vk_session = vk.VkApi(token=os.environ['VK_GROUP_ACCESS_TOKEN'])
    vk_api = vk_session.get_api()
    longpoll = VkLongPoll(vk_session)
    while True:
        try:
            for event in longpoll.listen():
                if event.type == VkEventType.MESSAGE_NEW and event.to_me:
                    message_reply(event, vk_api, project_id)
        except Exception as ex:
            print(ex)
            sleep(30)


if __name__ == '__main__':
    main()
