import telebot

from messages import default_messages_user, keyboards_user
from database import db_session
from database.party import Party
from database.programma import Programma
from database.organizators import Moder
from database.speakers import Speaker
from database.temas import Tema


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
                             'Программа будет проходить в течении несокльких дней\nНа какой день вы бы хотели узнать программу:',
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

    # Даёт расписание на день
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

    # Даёт список Модераторов
    @bot.callback_query_handler(func=lambda call: call.data.startswith("moder_num"))
    def select_moder(call):
        id_ivent = int(call.data.replace("moder_num", ""))
        moderators = db_sess.query(Moder).filter(Moder.id_party == id_ivent).all()
        bot.send_message(call.message.chat.id, "Список орагнизаторов:")
        for moder in moderators:
            des = moder.name
            keyb = telebot.types.InlineKeyboardMarkup()
            data = 'current_moder_id' + str(moder.id)
            keyb.add(telebot.types.InlineKeyboardButton(text="Узнать больше", callback_data=data))

            bot.send_message(call.message.chat.id, des, reply_markup=keyb)
        bot.send_message(message.chat.id, "Это все организаторы!", reply_markup=keyboards_user.get_go_to_main_menukb())

    # Даёт список Спикеров
    @bot.callback_query_handler(func=lambda call: call.data.startswith("speaker_num"))
    def select_moder(call):
        id_ivent = int(call.data.replace("speaker_num", ""))
        speakers = db_sess.query(Speaker).filter(Speaker.id_party == id_ivent).all()
        bot.send_message(call.message.chat.id, "Список спикеров:")
        for speaker in speakers:
            des = speaker.name
            keyb = telebot.types.InlineKeyboardMarkup()
            data = 'current_speaker_id' + str(speaker.id)
            keyb.add(telebot.types.InlineKeyboardButton(text="Узнать больше", callback_data=data))

            bot.send_message(call.message.chat.id, des, reply_markup=keyb)
        bot.send_message(message.chat.id, "Это все спикеры!", reply_markup=keyboards_user.get_go_to_main_menukb())

    # Даёт список тем
    @bot.callback_query_handler(func=lambda call: call.data.startswith("obs_num"))
    def select_moder(call):
        id_ivent = int(call.data.replace("obs_num", ""))
        temas = db_sess.query(Tema).filter(Tema.id_party == id_ivent).all()
        bot.send_message(call.message.chat.id, "Список тем:")
        msg = ""
        for tema in temas:
            msg += tema.comment + "\n"
        bot.send_message(call.message.chat.id, msg, reply_markup=keyboards_user.get_go_to_main_menukb())
    # Информация о конкретном спикере
    @bot.callback_query_handler(func=lambda call: call.data.startswith("current_speaker_id"))
    def select_moder(call):
        id_speaker = int(call.data.replace("current_speaker_id", ""))
        speaker = db_sess.query(Speaker).filter(Speaker.id == id_speaker).first()

        des = "Имя: " + speaker.name + "\n"
        des += "Немного о спикере: " + speaker.comment
        bot.send_message(call.message.chat.id, des, reply_markup=keyboards_user.get_go_to_main_menukb())

    # Информация о конкретном модере
    @bot.callback_query_handler(func=lambda call: call.data.startswith("current_moder_id"))
    def select_moder(call):
        id_moder = int(call.data.replace("current_moder_id", ""))
        moder = db_sess.query(Moder).filter(Moder.id == id_moder).first()

        des = "Имя: " + moder.name + "\n"
        des += "Немного о спикере: " + moder.comment
        bot.send_message(call.message.chat.id, des, reply_markup=keyboards_user.get_go_to_main_menukb())