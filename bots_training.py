from dotenv import load_dotenv
from google.cloud import dialogflow_v2beta1 as dialogflow
import os
import json


def read_json(file_path, file_name):
    full_filename = os.path.join(file_path, file_name)
    with open(full_filename, "r") as my_file:
        intents_json = my_file.read()
    intents = json.loads(intents_json)
    return intents


def create_intent(project_id, display_name, training_phrases_parts, message_texts):
    intents_client = dialogflow.IntentsClient()
    parent = dialogflow.AgentsClient.agent_path(project_id)
    training_phrases = []
    for training_phrases_part in training_phrases_parts:
        part = dialogflow.Intent.TrainingPhrase.Part(text=training_phrases_part)
        # Here we create a new training phrase for each provided part.
        training_phrase = dialogflow.Intent.TrainingPhrase(parts=[part])
        training_phrases.append(training_phrase)

    text = dialogflow.Intent.Message.Text(text=message_texts)
    message = dialogflow.Intent.Message(text=text)

    intent = dialogflow.Intent(
        display_name=display_name, training_phrases=training_phrases, messages=[message]
    )

    response = intents_client.create_intent(
        request={"parent": parent, "intent": intent}
    )

    print("Intent created: {}".format(response))


def main():
    load_dotenv()
    project_id = os.environ['GOOGLE_PROJECT_ID']
    file_path = os.getenv("QUESTIONS_PATH", os.getcwd())
    file_name = os.getenv("QUESTIONS_FILENAME", 'questions.json')
    itents = read_json(file_path, file_name)
    for itent_name, itent_cotnent in itents.items():
        texts = itent_cotnent['questions']
        answer = [itent_cotnent['answer']]
        create_intent(project_id, itent_name, texts, answer)


if __name__ == '__main__':
    main()
