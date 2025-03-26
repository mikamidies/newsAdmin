import logging
from telebot import TeleBot
from django.conf import settings
from api.models import Application


def send_application_to_telegram(applciation: Application):
    TEXT = f"Имя: {applciation.name}\nНомер: {applciation.phone}"

    try:
        bot = TeleBot(settings.BOT_TOKEN)
        chat_id = settings.CHAT_ID
        bot.send_message(chat_id, text=TEXT)

    except Exception as e:
        logging.error("Telegram Issues: {}".format(str(e)))
