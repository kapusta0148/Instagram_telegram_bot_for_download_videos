import telebot
from dotenv_func import dotenv
from download_functions import escape_md ,download_mp4_from_instagram


SECRET_KEY = dotenv('SECRET_KEY')
WELCOME_TEXT = dotenv('WELCOME_TEXT')
bot = telebot.TeleBot(SECRET_KEY)
bot.set_webhook()


@bot.message_handler(commands=['start'])
def start(message):
    name = message.from_user.first_name
    bot.send_message(message.chat.id, WELCOME_TEXT.format(name=name))


@bot.message_handler(func=lambda message: "instagram" in message.text)
def instagram_video_downloader(message):
    url = message.text
    url = escape_md(download_mp4_from_instagram(url))
    bot.send_message(
        message.chat.id,
        f'Видео загружается ожидайте[\\.]({url})',
        parse_mode="MarkdownV2"
    )


if __name__ == '__main__':
    bot.infinity_polling()