# Vk Чат-Бот с интегрированным DialogFlow.
 Бот использует API DialogFlow

## Описание
С помощью данного чат-бота можно организовать службу поддержки, которая отвечает на частозадаваемые вопросы пользователей 

## Требования
Для работы должен быть установлен python3. А также необходимо установить библиотеки, python-dotenv, 
google-cloud-dialogflow, vk_api  которые описаны в файле requirements.txt
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
* TVK_TOKEN_ID='vk1.a.xHTLvJ-eaJue--VkA4D8a7AKisj8oHq6rrdN5znMP9jb1SfwQ_uM_Hs6vuhGvfRjBMNb5AYFzbOse9CU4vXWqoEiLmLgkzaGJ4QsYHzOv06FLWugDpKaG2Q_uxR0b5GFGU-vhNbY-Yy3KO5c2U3yFKCJgH-nOSopLJceJPAABYXuPpDqa7xUoh1ns17H1O8uTlD-05jS49ECGyfyqDtxY_g'
* VK_USER_ID= -id пользователя vkontakte
* VK_GROUP_ID= -id группы вконтакте
* VK_GROUP_ACCESS_TOKEN= -токен группы вконтакте

## Пример запуска скрипта
```bash
python main.py
```

Для проверки результата нужно написать сообщение в группу VK_GROUP_ID.