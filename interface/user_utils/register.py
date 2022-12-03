import telebot
from database.users_reg import UserReg

from messages import default_messages_user, keyboards_user
from interface.user_utils import register


def step_name(message, bot: telebot.TeleBot, user: UserReg):
    bot.send_message(message.chat.id, "Введите своё имя:")
    name = ""


    return
