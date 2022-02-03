import os
import time
from threading import Thread

import schedule
import telebot
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.environ['TOKEN']
FILE_PATH = int(os.environ['FILE_PATH'])

bot = telebot.TeleBot(TOKEN)

ADMIN_OWNER = os.environ['OWNER_ID']


def schedule_checker():
    while True:
        schedule.run_pending()
        time.sleep(1)


def get_valid_ids(message):
    chat_id = message.chat.id
    chat_administrators = bot.get_chat_administrators(chat_id)
    return [admin.user.id for admin in chat_administrators]


@bot.message_handler(commands=['schedule_polls'])
def handle_polls(message):
    allowed_ids = get_valid_ids(message)

    if message.from_user.id in allowed_ids or message.from_user.id == ADMIN_OWNER:

        poll_question = 'Did you attend Communion Service?'
        options = ['Yes', 'No']
        schedule.every().Thursday.at('10:00').do(
            bot.send_poll, chat_id=message.chat.id, question=poll_question, options=options)

        bot.reply_to(message, 'Polls have been scheduled')

    else:
        bot.reply_to(message, 'Sorry you can\'t send this command')


@bot.message_handler(commands=['stop_polls'])
def stop_polls(message):
    allowed_ids = get_valid_ids(message)
    if message.from_user.id in allowed_ids or message.from_user.id == ADMIN_OWNER:
        schedule.cancel_job()


Thread(target=schedule_checker, daemon=True).start()

bot.infinity_polling()
