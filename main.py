import os

import telebot

from dotenv_func import dotenv
from download_functions import (
    TELEGRAM_FILE_LIMIT,
    download_video,
    escape_md,
    get_video_url_via_rapidapi,
)

SECRET_KEY = dotenv('SECRET_KEY')
WELCOME_TEXT = dotenv('WELCOME_TEXT')
RAPIDAPI_KEY = dotenv('RAPIDAPI_KEY')

bot = telebot.TeleBot(SECRET_KEY)
bot.remove_webhook()


@bot.message_handler(commands=['start'])
def start(message):
    name = message.from_user.first_name
    bot.send_message(message.chat.id, WELCOME_TEXT.format(name=name))


@bot.message_handler(func=lambda message: "instagram" in message.text)
def instagram_video_downloader(message):
    chat_id = message.chat.id
    url = message.text.strip()
    bot.send_message(chat_id, 'Видео загружается, ожидайте…')

    path = None
    try:
        video_url = get_video_url_via_rapidapi(url, RAPIDAPI_KEY)

        path = download_video(video_url)

        if os.path.getsize(path) <= TELEGRAM_FILE_LIMIT:
            with open(path, 'rb') as video:
                bot.send_video(chat_id, video)
        else:
            link = escape_md(video_url)
            bot.send_message(
                chat_id,
                f'Видео больше 50 МБ — скачайте по ссылке: [тык]({link})',
                parse_mode='MarkdownV2',
            )
    except Exception:
        bot.send_message(chat_id, 'Не удалось скачать это видео 😔')
    finally:
        if path and os.path.exists(path):
            os.remove(path)


if __name__ == '__main__':
    bot.infinity_polling()
