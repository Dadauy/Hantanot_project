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
    bot.send_message(call.message.chat.id, 'сюда нужно вставить описание бота',
                     reply_markup=keyboards.get_go_to_main_menukb())


@bot.callback_query_handler(func=lambda call: call.data == 'main_menu')
def start_main_menu(call):
    bot.send_message(call.message.chat.id, 'Добро Пожаловать в основное меню!')
    for punct in default_messages.MAIN_MENU:
        bot.send_message(call.message.chat.id, punct)
    msg = bot.send_message(call.message.chat.id, 'Выберите интересующий вас пункт:', reply_markup=keyboards.get_mainkb())
    bot.register_next_step_handler(msg, choice)

# main menu
def choice(message):
    pass



#


bot.enable_save_next_step_handlers(delay=2)
bot.load_next_step_handlers()
bot.infinity_polling()
