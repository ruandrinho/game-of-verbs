# game-of-verbs
 
Боты для общения с клиентами в Telegram и VK.

![demo_tg_bot](https://user-images.githubusercontent.com/84133942/178480441-346e0a3a-520f-4722-8d58-12b1efafc07f.gif)

![demo_vk_bot](https://user-images.githubusercontent.com/84133942/178480461-345f437c-3b8c-4d9b-a7da-f1ada4152c1e.gif)

## Как установить

Клонируйте репозиторий или скачайте архив и распакуйте.

Создайте файл окружения `.env` и заполните необходимым данными:
```
TELEGRAM_BOT_TOKEN=
TELEGRAM_LOGGING_CHAT_ID=
VK_BOT_GROUP_ID=
VK_BOT_TOKEN=
GOOGLE_APPLICATION_CREDENTIALS=
GOOGLECLOUD_PROJECT_ID=
```

Python3 должен быть уже установлен. 
Затем используйте `pip` (или `pip3`, есть конфликт с Python2) для установки зависимостей:
```
pip install -r requirements.txt
```

## Запуск скриптов

```
python vkbot.py
python tgbot.py
```

## Деплой на Heroku

Скрипт полностью готов к деплою. Сделайте форк репозитория, создайте новое приложение на Heroku, после чего в разделе Settings:
1. Подключите приложение к своему репозиторию
2. Задайте те же Config Vars, что и для файла .env
3. Создайте два buildpacks:
   - heroku/python
   - https://github.com/gerywahyunugraha/heroku-google-application-credentials-buildpack
4. Нажмите на кнопку Deploy Branch

## Цель проекта

Код написан в образовательных целях на онлайн-курсе для веб-разработчиков [dvmn.org](https://dvmn.org/).
