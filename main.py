import os
import time
from threading import Thread

from helper import polls_result_text
import schedule
import telebot
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.environ['TOKEN']
FILE_PATH = int(os.environ['FILE_PATH'])

bot = telebot.TeleBot(TOKEN)

GS = os.environ['GS']
AGS = os.environ['AGS']


def schedule_checker():
    while True:
        schedule.run_pending()
        time.sleep(1)


def get_valid_ids(message):
    chat_id = message.chat.id
    chat_administrators = bot.get_chat_administrators(chat_id)

    return [admin.user.id for admin in chat_administrators]


@bot.message_handler(commands=['send_polls'])
def handle_polls(message):
    allowed_ids = get_valid_ids(message)
    allowed_ids += [GS, AGS]

    if message.from_user.id in allowed_ids:

        poll_question = 'Did you attend Communion Service?'
        options = ['Yes', 'No']
        schedule.every().Thursday.at('10:00').do(
            bot.send_poll, chat_id=message.chat.id, question=poll_question, options=options)

        bot.reply_to(message, 'Polls have been scheduled')

    else:
        bot.reply_to(message, 'Sorry you can\'t send this command')

        schedule.every().Friday.at('21:00').do(bot.send_message, chat_id=[AGS, GS], f)

@bot.message.handler(commands=['stop_polls'])
def stop_polls(message):


@bot.message_handler(commands=['stop_polls'])
def stop_polls(message):
    allowed_ids = get_valid_ids(message)
    if message.from_user.id in allowed_ids or message.from_user.id == AGS:
        schedule.cancel_job()


Thread(target=schedule_checker, daemon=True).start()

bot.infinity_polling()
