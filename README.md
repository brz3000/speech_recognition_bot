# Vk и Telegram Чат-Бот с интегрированным DialogFlow.
 Бот использует API DialogFlow

## Описание
С помощью данных чат-ботов можно организовать службу поддержки, которая отвечает на часто задаваемые вопросы пользователей 

## Требования
Для работы должен быть установлен python3. А также необходимо установить библиотеки, python-dotenv, 
google-cloud-dialogflow, vk_api и python-telegram-bot которые описаны в файле requirements.txt
Чтобы установить python3 скачайте и ознакомьтесь с инструкцией по установке на сайте [python.org](https://www.python.org/downoloads)

## Установка
Необходимые библиотеки устанавливается командой:
```bash
pip install -r requirement.txt
```

## Настройки
Необходимо чтобы в дирректории проекта был файл .env, в котором содержаться переменные окружения:
* GOOGLE_PROJECT_ID= - узнать можно в профиле на [https://dialogflow.cloud.google.com/#/agent]
* GOOGLE_APPLICATION_CREDENTIALS= - Путь, где лежит credentials.json путь до файла с ключами от Google, как получить описано тут [https://cloud.google.com/api-keys/docs/get-started-api-keys]
* DIALOGFLOW_API_KEY= - ключ DialogFlow, описание как получить тут [https://cloud.google.com/docs/authentication/api-keys].
* VK_TOKEN_ID=  - токен пользователя
* VK_USER_ID= -id пользователя vkontakte
* VK_GROUP_ID= -id группы вконтакте
* VK_GROUP_ACCESS_TOKEN= -токен группы вконтакте
* TLG_TOKEN_LOGGER_BOT= -токен телеграм бота, который присылает логи, узнать можно у @BotFather.
* TLG_CHAT_ID= id чата с ботом. Узнать можно написав @userinfobot
  
## Обучение бота новым вопросам и ответам
Для того чтобы не редактировать вручную вопросы\ответы от бота, в web интерфейсе DialogFlow предусмотрен режим обучения ботов через API.
Для этого необходимо указать где расположен файл с вопросами и ответами.
Необходимо в файле .env прописать две переменные:
* QUESTIONS_FILENAME= -имя файла
* QUESTIONS_PATH= -путь до рабочей директории с файлом.

Файл с заготовленными фразами должен иметь структуру JSON. 

Если не указывать переменные окружения QUESTIONS_FILENAME и QUESTIONS_PATH, по умолчанию будет выбрана текущая папка с проектом и именем файла "questions.json".
В репозитории приведён пример questions.json с фразами.

Далее для обучения необходимо запустить файл bots_training.py.

```bash
python bots_training.py
```


## Пример запуска VK-бота 
```bash
python vk_bot.py
```


## Пример запуска Telegram-бота 
```bash
python tg_bot.py
```
Для проверки результата нужно написать сообщение в группу VK_GROUP_ID или в телеграм боту https://t.me/dvmn_brz_notify_bot.

![vk_dialogflow](https://github.com/brz3000/speech_recognition_bot/assets/45814758/57d22e23-13b9-43d4-8ea5-7b5c3fac6b94)
