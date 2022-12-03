import telebot

from messages import default_messages_user, keyboards_user

speakers = [
    {
        'speaker_id': 1,
        'name': 'speaker1',
        'work': 'job1'
    },
    {
        'speaker_id': 2,
        'name': 'speaker2',
        'work': 'job2'
    },
]


def user(bot: telebot.TeleBot, message):
    # Стартовое приветствие
    bot.send_message(message.chat.id, default_messages_user.HELLO_MESSAGE)
    bot.send_message(message.chat.id, "Хотите узнать обо мне побольше?", reply_markup=keyboards_user.get_welcomekb())

    # callback handlers
    @bot.callback_query_handler(func=lambda call: call.data == 'about')  # Обработка кнопки описания
    def callback_about(call):
        bot.send_message(call.message.chat.id,
                         'Я бот созданный для ITфорума, я могу вывести всю информацию о нём и зарегистрировать вас туда',
                         reply_markup=keyboards_user.get_go_to_main_menukb())

    @bot.callback_query_handler(
        func=lambda call: call.data == 'main_menu')  # обработка кнопки перезода к основному меню
    def start_main_menu(call):  # Вывод основного меню с клавиатурой
        bot.send_message(call.message.chat.id, 'Добро Пожаловать в основное меню!')
        menu = ""
        for punct in default_messages_user.MAIN_MENU:
            menu += punct + "\n"
        bot.send_message(call.message.chat.id, menu)  # Отправляем меню пользователю

        msg = bot.send_message(call.message.chat.id, 'Выберите интересующий вас пункт:',
                               reply_markup=keyboards_user.get_mainkb())
        bot.register_next_step_handler(msg, choice)  # Переход на следующий шаг взаимодействия с menu

    # main menu
    def choice(message):
        id = message.text

        if id == default_messages_user.emojicode['1']:
            bot.send_message(message.chat.id, "Название мероприятия, участники и опсиание",
                             reply_markup=keyboards_user.get_go_to_main_menukb())  # вывели инфу и предложили вернуться в галвное меню
            return
        if id == default_messages_user.emojicode['2']:
            bot.send_message(message.chat.id, "Тематические разделы проекта",
                             reply_markup=keyboards_user.get_go_to_main_menukb())  # вывели инфу и предложили вернуться в галвное меню
            return
        if id == default_messages_user.emojicode['3']:
            bot.send_message(message.chat.id, 'Краткая информация о спикерах')
            for speaker in speakers:
                # Создаём клавиатуру для инфы про спикеров
                keyb = telebot.types.InlineKeyboardMarkup()
                data = "speaker_number:" + str(speaker['speaker_id'])
                btn = telebot.types.InlineKeyboardButton(text="Узнать больше",
                                                         callback_data=data)
                keyb.add(btn)
                bot.send_message(message.chat.id,
                                 str(speaker['speaker_id']) + " " + speaker['name'] + " " + speaker['work'],
                                 reply_markup=keyb)
            return

        # если пользователь что-то написал, а не нажал на клавиатуру
        msg = bot.send_message(message.chat.id, "Введены некоректные данные\nПожалуйста воспользуйтесь клавиатурой",
                               reply_markup=keyboards_user.get_mainkb())
        bot.register_next_step_handler(msg, choice)

    @bot.callback_query_handler(func=lambda call: call.data.startswith("speaker_number:"))
    def get_speaker_info(call):

        bot.send_message(call.message.chat.id, "Информация о спикере с id: " + call.data.replace("speaker_number:", ""),
                         reply_markup=keyboards_user.get_go_to_main_menukb())

    #

    bot.enable_save_next_step_handlers(delay=2)
    bot.load_next_step_handlers()
