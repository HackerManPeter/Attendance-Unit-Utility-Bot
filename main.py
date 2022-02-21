import os
import time
from threading import Thread

from helper import send_polls, get_valid_ids

from schedule import every, run_pending, clear
import telebot
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.environ["TOKEN"]

bot = telebot.TeleBot(TOKEN)


def schedule_checker():
    while True:
        run_pending()
        time.sleep(1)


@bot.message_handler(commands=["send_polls"])
def handle_polls(message):
    allowed_ids = get_valid_ids(message)
    if message.from_user.id not in allowed_ids:
        bot.reply_to(
            message,
            f"Sorry {message.from_user.first_name}, you are not authorised to send this command",
        )
        return

    bot.reply_to(message, "Polls have been scheduled")

    # every().thursday.at("9:00").do(send_polls, message)
    every(30).seconds.do(send_polls, message).tag("Polling")


@bot.message_handler(commands=["stop_polls"])
def stop_polls(message):
    allowed_ids = get_valid_ids(message)
    if message.from_user.id not in allowed_ids:
        bot.reply_to(
            message,
            f"Sorry {message.from_user.first_name}, you are not authorised to send this command",
        )
        return

    clear("Polling")
    bot.reply_to(message, "Polls have been stopped")


Thread(target=schedule_checker, daemon=True).start()

bot.infinity_polling()
