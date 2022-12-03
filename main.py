from interface import user_interface, admin_interface
from messages import default_messages_user, keyboards_user
from database import db_session
from settings.config import BOT_TOKEN
import telebot
from database.man_law import ManLaw
import sqlalchemy
import os

# init
bot = telebot.TeleBot(BOT_TOKEN)


# message handlers
@bot.message_handler(commands=['start'])  # Вывод приветственной клавиатуры
def start_hello(message):
    db_session.global_init("db/db_forum.db")
    db_sess = db_session.create_session()
    res = db_sess.query(ManLaw).filter(ManLaw.id_tg == message.chat.id).first()  # данные о юзере
    if res.law == 0:  # если обычный пользователь
        user_interface.user(bot, message)
    elif res.law == 1:  # если админe
        admin_interface.admin(bot, message)


bot.infinity_polling()
