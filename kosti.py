import default_messages
import keyboards
from config import BOT_TOKEN
import telebot

# init
bot = telebot.TeleBot(BOT_TOKEN)


#


# message handlers
@bot.message_handler(commands=['start'])
def start_hello(message):
    bot.send_message(message.from_user.id, default_messages.HELLO_MESSAGE)
    bot.send_message(message.from_user.id, "Хотите узнать обо мне побольше?", reply_markup=keyboards.get_welcomekb())


# callback handlers
@bot.callback_query_handler(func=lambda call: call.data == 'about')
def callback_about(call):
    bot.send_message(call.message.chat.id, 'сюда нужно вставить описание бота')


bot.infinity_polling()
