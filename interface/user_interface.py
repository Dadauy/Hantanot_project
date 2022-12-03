from messages import default_messages_user, keyboards_user


def user(bot, message):
    bot.send_message(message.chat.id, default_messages_user.HELLO_MESSAGE)
    bot.send_message(message.chat.id, "Хотите узнать обо мне побольше?", reply_markup=keyboards_user.get_welcomekb())

    # callback handlers
    @bot.callback_query_handler(func=lambda call: call.data == 'about')  # Обработка кнопки описания
    def callback_about(call):
        bot.send_message(call.message.chat.id, 'сюда нужно вставить описание бота',
                         reply_markup=keyboards_user.get_go_to_main_menukb())

    @bot.callback_query_handler(
        func=lambda call: call.data == 'main_menu')  # обработка кнопки перезода к основному меню
    def start_main_menu(call):  # Вывод основного меню с клавиатурой
        bot.send_message(call.message.chat.id, 'Добро Пожаловать в основное меню!')
        menu = ""
        for punct in default_messages_user.MAIN_MENU:
            menu += punct + "\n"
        bot.send_message(call.message.chat.id, menu)
        msg = bot.send_message(call.message.chat.id, 'Выберите интересующий вас пункт:',
                               reply_markup=keyboards_user.get_mainkb())
        bot.register_next_step_handler(msg, choice)  # Переход на следующий шаг взаимодействия с menu

    # main menu
    def choice(message):
        pass

    #

    bot.enable_save_next_step_handlers(delay=2)
    bot.load_next_step_handlers()
