import telebot
from dotenv_func import dotenv


SECRET_KEY = dotenv('SECRET_KEY')
WELCOME_TEXT = dotenv('WELCOME_TEXT')
bot = telebot.TeleBot(SECRET_KEY)
bot.set_webhook()


@bot.message_handler(commands=['start'])
def start(message):
    name = message.from_user.first_name
    bot.send_message(message.chat.id, WELCOME_TEXT.format(name=name))


@bot.message_handler(content_types=['text'])
def url_processing(message):
    url = message.text
    url = url.replace('www.', 'kk', 1)
    bot.send_message(message.chat.id, url)


if __name__ == '__main__':
    bot.infinity_polling()