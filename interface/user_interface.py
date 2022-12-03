import telebot

from messages import default_messages_user, keyboards_user
from database import db_session
from database.party import Party
from database.programma import Programma


def user(bot: telebot.TeleBot, message, db_sess):
    # Стартовое приветствие
    bot.send_message(message.chat.id, default_messages_user.HELLO_MESSAGE)
    bot.send_message(message.chat.id, "Хотите узнать обо мне побольше?", reply_markup=keyboards_user.get_welcomekb())

    # callback handlers
    @bot.callback_query_handler(func=lambda call: call.data == 'about')  # Обработка кнопки описания
    def callback_about(call):
        bot.send_message(call.message.chat.id,
                         'Я бот созданный спеицально для IT-форума, я могу вывести всю информацию о нём и зарегистрировать вас туда',
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
        # choice(msg)

    # main menu
    def choice(message):
        id = message.text

        if id == default_messages_user.emojicode['1']:
            ivent = db_sess.query(Party).get(1)
            description = default_messages_user.get_decription(party=ivent)

            bot.send_message(message.chat.id, description,
                             reply_markup=keyboards_user.get_go_to_main_menukb())  # вывели инфу и предложили вернуться в галвное меню
            return
        if id == default_messages_user.emojicode['2']:
            bot.send_message(message.chat.id,
                             'Программа будет проходить в течении несокльких дней\nНа какой день вы бы хотели узнать программу',
                             reply_markup=keyboards_user.get_daykb(db_sess.query(Programma).all()))

            return
        if id == default_messages_user.emojicode['3']:
            pass

        # если пользователь что-то написал, а не нажал на клавиатуру
        msg = bot.send_message(message.chat.id,
                               "Введены некоректные данные{}\nПожалуйста воспользуйтесь клавиатурой{}".format(
                                   default_messages_user.emojicode["confused"],
                                   default_messages_user.emojicode["smile"]),
                               reply_markup=keyboards_user.get_mainkb())
        bot.register_next_step_handler(msg, choice)

    @bot.callback_query_handler(func=lambda call: call.data.startswith("day_num"))
    def select_day(call):
        day_num = int(call.data.replace("day_num", ""))
        bot.send_message(call.message.chat.id, "Расписание на день:")
        ivents = db_sess.query(Programma).all()

        for ivent in ivents:
            if ivent.date_start.day == day_num:
                des = default_messages_user.get_ivent_description(ivent)
                bot.send_message(call.message.chat.id, des, reply_markup=keyboards_user.get_kb_for_programma(ivent.id))
        bot.send_message(call.message.chat.id, "Вот все мероприятия на этот день!",
                         reply_markup=keyboards_user.get_go_to_main_menukb())


