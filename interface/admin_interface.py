import telebot
from messages import default_messages_admin, keyboards_admin
from messages import keyboards_admin


def admin(bot: telebot.TeleBot, message):
    start_menu = telebot.types.ReplyKeyboardMarkup(True, True)
    start_menu.add('Администратора', 'Организатора', "Спикера", "Частых вопросов", "Мероприятия")
    bot.send_message(message.chat.id, default_messages_admin.HELLO_MESSAGE, reply_markup=start_menu)

    @bot.callback_query_handler(func=lambda call: call.data == 'about')  # Обработка кнопки описания
    def callback_about(call):
        bot.send_message(call.message.chat.id, "hello", reply_markup=keyboards_admin.menucb())
