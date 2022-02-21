import os
import telebot
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.environ["TOKEN"]

bot = telebot.TeleBot(TOKEN)

# GS = os.environ["GS"]
AGS = os.environ["AGS"]


def send_polls(message):
    poll_question = "Did you attend Communion Service?"
    options = ["Yes", "No"]
    poll_response = bot.send_poll(
        chat_id=message.chat.id,
        question=poll_question,
        options=options,
        is_anonymous=False,
    )

    bot.forward_message(
        chat_id=AGS, from_chat_id=poll_response.chat.id, message_id=poll_response.id
    )


def get_valid_ids(message):
    chat_id = message.chat.id
    chat_administrators = bot.get_chat_administrators(chat_id)
    valid_ids = [admin.user.id for admin in chat_administrators]
    return valid_ids + [AGS]


# def invalid_message(message):
#     allowed_ids = get_valid_ids(message)

#     if message.from_user.id not in allowed_ids:
#         bot.reply_to(
#             message,
#             f"Sorry {message.from_user.first_name}, you are not authorised to send this command",
#         )
#         return False
#     return True
