import telebot
import schedule
from threading import Thread
from time import sleep

from messages import default_messages_user, keyboards_user
from sqlalchemy.orm import Session
from database import db_session
from database.party import Party
from database.programma import Programma
from database.organizators import Moder
from database.speakers import Speaker
from database.temas import Tema
from database.users_reg import UserReg
from database.inter_party import InterParty
from database.inter_party_reg import InterPartyReg
from database.best_questions import BestQuestion
from database.quests import Quest
from database.all_users import AllUsers
import datetime


def checker():
    while True:
        schedule.run_pending()
        sleep(1)


def user(bot: telebot.TeleBot, message: telebot.types.Message, db_sess: Session):
    # Проверка токена:
    current_user: AllUsers = db_sess.query(AllUsers).filter(AllUsers.chat_id == message.chat.id).first()
    if current_user.code == "0":
        bot.send_message(message.chat.id, "Введите пожалуйста код!")

        @bot.message_handler(content_types=['text'])
        def check_code(message: telebot.types.Message):
            if message.text.startswith("it2023#"):
                current_user.code = message.text
                db_sess.commit()
                # Стартовое приветствие
                bot.send_message(message.chat.id, default_messages_user.HELLO_MESSAGE,
                                 reply_markup=keyboards_user.get_go_to_main_site_and_main_menu())

            else:
                bot.send_message(message.chat.id, "Ваш код недействителен, перейдите на сайт для получения кода.",
                                 reply_markup=keyboards_user.get_go_to_main_site())

        return
    else:
        # Стартовое приветствие
        bot.send_message(message.chat.id, default_messages_user.HELLO_MESSAGE,
                         reply_markup=keyboards_user.get_go_to_main_site_and_main_menu())

    # !timer!
    day_to_start = datetime.timedelta(days=0)
    res = db_sess.query(Programma).first()

    if res != None:
        start_date = res.date_start
        date_now = datetime.datetime.now()
        day_to_start = start_date - date_now

    def check_days():
        def send_function():
            data = ""
            if day_to_start.days == 7:
                data = "!ВНИМАНИЕ До начала форума осталась неделя!"
            if day_to_start.days == 3:
                data = "!ВНИМАНИЕ До начала форума осталось 3 дня!"
            if day_to_start.days == 1:
                data = "!ВНИМАНИЕ До начала форума остался один день!"
            rusers = db_sess.query(UserReg).all()
            for user in rusers:
                bot.send_message(user.id_tg, data)

        return send_function

    schedule.every().day.at('00:00').do(check_days())

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
            id = message.chat.id
            user_r = db_sess.query(UserReg).filter(UserReg.id_tg == id).first()
            if user_r == None:
                bot.send_message(message.chat.id,
                                 "Я оповещу вас о начале Мероприятия за неделю, за 3 дня, за час, но для этого вам нужно зарегистрироваться(5 пункт главного меню)",
                                 reply_markup=keyboards_user.get_go_to_main_menukb())
            else:
                bot.send_message(message.chat.id,
                                 "Вы уже заргеистрированы, я оповещу вас о начале мероприятия!{}".format(
                                     default_messages_user.emojicode['smile']),
                                 reply_markup=keyboards_user.get_go_to_main_menukb())
            return
        if id == default_messages_user.emojicode['4']:
            bot.send_message(message.chat.id, "Выберите пункт:", reply_markup=keyboards_user.get_menu_quest())
            return

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
        ivents: list[Programma] = db_sess.query(Programma).all()
        ucls = False
        expo = False
        for ivent in ivents:
            if ivent.date_start.day == day_num:
                if ivent.place.startswith("КТЦ"):
                    ucls = True
                elif ivent.place.startswith("КВЦ"):
                    expo = True
        if ucls and expo:
            bot.send_message(call.message.chat.id, "Выберите место проведения:",
                             reply_markup=keyboards_user.get_places_kb(1, day_num))
        elif ucls:
            bot.send_message(call.message.chat.id, "Выберите место проведения:",
                             reply_markup=keyboards_user.get_places_kb(2, day_num))
        elif expo:
            bot.send_message(call.message.chat.id, "Выберите место проведения:",
                             reply_markup=keyboards_user.get_places_kb(3, day_num))

    @bot.callback_query_handler(func=lambda call: call.data.startswith("prog"))
    def get_program_for_day(call):
        type = int(call.data.replace("prog", "").split("*")[1])
        place = ""
        if type == 1:
            place = "КТЦ"
        elif type == 2:
            place = "КВЦ"
        day = int(call.data.replace("prog", "").split("*")[0])
        bot.send_message(call.message.chat.id, "Расписание на день:")
        ivents = db_sess.query(Programma).all()
        for ivent in ivents:
            if ivent.date_start.day == day and ivent.place.startswith(place):
                des = default_messages_user.get_ivent_description(ivent)
                bot.send_message(call.message.chat.id, des, parse_mode="HTML")

        bot.send_message(call.message.chat.id, "Вот все мероприятия на этот день!",
                         reply_markup=keyboards_user.get_go_to_main_menukb())

    # Вывод маленьких событий
    @bot.callback_query_handler(func=lambda call: call.data == 'reg_ivents')
    def send_ivents(call):
        ivents = db_sess.query(InterParty).all()

        for ivent in ivents:
            data = default_messages_user.get_info_ivent(ivent)
            kb = telebot.types.InlineKeyboardMarkup()
            cdata = "ivent_for_reg" + str(ivent.id)
            btn = telebot.types.InlineKeyboardButton(text="Зарегистрироваться", callback_data=cdata)
            kb.add(btn)
            bot.send_message(call.message.chat.id, data, reply_markup=kb)

    # Обработчик запросов на регистрацию
    @bot.callback_query_handler(func=lambda call: call.data.startswith('ivent_for_reg'))
    def try_reg(call):
        ivent_id = int(call.data.replace('ivent_for_reg', ''))
        ivent = db_sess.query(InterParty).filter(InterParty.id == ivent_id).first()
        list_reg = db_sess.query(InterPartyReg).filter(InterPartyReg.chatid == call.message.chat.id).all()
        if list_reg != None:
            for reg in list_reg:
                if reg.id_party == ivent.id:
                    bot.send_message(call.message.chat.id, "Вы уже зарегистрированы!",
                                     reply_markup=keyboards_user.get_other_ivents())
                    return
        if int(ivent.man_now) >= int(ivent.man_max):
            bot.send_message(call.message.chat.id,
                             "Все места уже заняты!{}".format(default_messages_user.emojicode['confused']),
                             reply_markup=keyboards_user.get_other_ivents())
            return
        reg = InterPartyReg(id_party=ivent_id, chatid=call.message.chat.id)
        ivent.man_now = ivent.man_now + 1
        db_sess.add(ivent)
        db_sess.add(reg)
        db_sess.commit()
        bot.send_message(call.message.chat.id, "Вы успешно зарегистрирваны",
                         reply_markup=keyboards_user.get_other_ivents())

    # Вывод частозадаваемых вопросов
    @bot.callback_query_handler(func=lambda call: call.data.startswith('bestq'))
    def get_bestquestion(call):
        bq_list = db_sess.query(BestQuestion).all()
        for quest in bq_list:
            bot.send_message(call.message.chat.id, "Вопрос: " + quest.quest + "\n" + "Ответ: " + quest.response)
        bot.send_message(call.message.chat.id, "Если не нашли свой вопрос здесь, можете задать вопрос самостоятельно!",
                         reply_markup=keyboards_user.get_menu_quest())

    # Задаём вопрос
    @bot.callback_query_handler(func=lambda call: call.data.startswith('quest'))
    def ask_quest(call):
        quest = Quest(chat_id=str(call.message.chat.id))
        bot.send_message(call.message.chat.id, "Задайте свой вопрос!")

        @bot.message_handler(content_types=['text'])
        def get_quest(message):
            quest.quest = message.text
            db_sess.add(quest)
            db_sess.commit()
            bot.send_message(message.chat.id, "Вопрос был отправлен оранизаторам, и скоро вам придёт ответ",
                             reply_markup=keyboards_user.get_menu_quest())

    scheduleThread = Thread(target=checker)
    scheduleThread.daemon = True
    scheduleThread.start()
