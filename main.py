from interface import user_interface, admin_interface
from messages import default_messages_user, keyboards_user
from settings.config import BOT_TOKEN
import telebot

# init
bot = telebot.TeleBot(BOT_TOKEN)


# message handlers
@bot.message_handler(commands=['start'])  # Вывод приветственной клавиатуры
def start_hello(message):
    user_interface.user(bot, message)


bot.infinity_polling()