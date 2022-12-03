import default_messages
from config import BOT_TOKEN
import telebot

# init
bot = telebot.TeleBot(BOT_TOKEN)
#

@bot.message_handler(commands=['start'])
def start_hello(message):
    bot.send_message(message.from_user.id, default_messages.HELLO_MESSAGE)




bot.infinity_polling()