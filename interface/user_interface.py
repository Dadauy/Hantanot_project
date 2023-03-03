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

global user_reg
user_reg = UserReg()


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
        if id == default_messages_user.emojicode['5']:
            if db_sess.query(UserReg).filter(UserReg.id_tg == message.chat.id).first() == None:
                msg = bot.send_message(message.chat.id,
                                       "Начало регистрации{}\nВведите своё имя:".format(
                                           default_messages_user.emojicode['pen']))

                user_reg.id_tg = message.chat.id
                bot.register_next_step_handler(msg, step_name)
            else:
                bot.send_message(message.chat.id, "Вы уже зарегестрированы на IT-форум!\n",
                                 reply_markup=keyboards_user.get_other_ivents())
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
                if ivent.place.startswith("КТЦ «Югра-Классик»"):
                    ucls = True
                elif ivent.place.startswith("КВЦ «Югра-Экспо»"):
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
            place = "КТЦ «Югра-Классик»"
        elif type == 2:
            place = "КВЦ «Югра-Экспо»"
        day = int(call.data.replace("prog", "").split("*")[0])
        bot.send_message(call.message.chat.id, "Расписание на день:")
        ivents = db_sess.query(Programma).all()
        for ivent in ivents:
            if ivent.date_start.day == day and ivent.place.startswith(place):
                des = default_messages_user.get_ivent_description(ivent)
                bot.send_message(call.message.chat.id, des)

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
    def select_speaker(call):
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

    # Шаги регистрации
    def step_name(message):
        user_reg.name = message.text
        msg = bot.send_message(message.chat.id, "Введите свою фамилию:")
        bot.register_next_step_handler(msg, step_surname)

    def step_surname(message):
        user_reg.surname = message.text
        msg = bot.send_message(message.chat.id, "Введите своё отчество:")
        bot.register_next_step_handler(msg, step_patronymic)

    def step_patronymic(message):
        user_reg.patronymic = message.text
        msg = bot.send_message(message.chat.id, "Введите своё имя на английском:")
        bot.register_next_step_handler(msg, step_name_eng)

    def step_name_eng(message):
        user_reg.name_eng = message.text
        msg = bot.send_message(message.chat.id, "Введите свою фамилию на английском:")
        bot.register_next_step_handler(msg, step_surname_eng)

    def step_surname_eng(message):
        user_reg.surname_eng = message.text
        msg = bot.send_message(message.chat.id, "Введите место работы:")
        bot.register_next_step_handler(msg, step_work)

    def step_work(message):
        user_reg.organization = message.text
        msg = bot.send_message(message.chat.id, "Введите формат: очно/заочно",
                               reply_markup=keyboards_user.get_formatkb())
        bot.register_next_step_handler(msg, step_format)

    def step_format(message):
        if message.text == 'очно':
            user_reg.format_challenge = True
        else:
            user_reg.format_challenge = False
        msg = bot.send_message(message.chat.id, "Вы из СМИ: да/нет",
                               reply_markup=keyboards_user.get_smi())
        bot.register_next_step_handler(msg, step_smi)

    def step_smi(message):
        if message.text == 'да':
            user_reg.in_smi = True
        else:
            user_reg.in_smi = False
        msg = bot.send_message(message.chat.id, "Введите название страны, где вы живёте:")
        bot.register_next_step_handler(msg, step_country)

    def step_country(message):
        user_reg.country = message.text
        msg = bot.send_message(message.chat.id, "Введите название города, где вы живёте:")
        bot.register_next_step_handler(msg, step_city)

    def step_city(message):
        user_reg.city = message.text
        msg = bot.send_message(message.chat.id, "Введите email:")
        bot.register_next_step_handler(msg, step_email)

    def step_email(message):
        user_reg.email = message.text
        msg = bot.send_message(message.chat.id, "Введите номер телефона:")
        bot.register_next_step_handler(msg, step_number)

    def step_number(message):
        user_reg.number = message.text
        msg = bot.send_message(message.chat.id, "Введите язык на котором разговариваете:")
        bot.register_next_step_handler(msg, step_language)

    def step_language(message):
        user_reg.language = message.text
        msg = bot.send_message(message.chat.id, "Вы согласны на обработку ваших данных: да/нет",
                               reply_markup=keyboards_user.get_smi())
        bot.register_next_step_handler(msg, step_agreement)

    def step_agreement(message):
        if message.text == 'да':
            user_reg.agreement = True
        else:
            user_reg.agreement = False
        msg = bot.send_message(message.chat.id, "Кажется это всё...", reply_markup=keyboards_user.get_next())
        bot.register_next_step_handler(msg, step_accept)

    def step_accept(message):

        data = "Регистрация завершена!\nПроверьте данные, которые ввели:\n" + default_messages_user.get_data(
            user_reg) + "\nДанные корректны?"
        msg = bot.send_message(message.chat.id, data, reply_markup=keyboards_user.get_acceptkb())
        bot.register_next_step_handler(msg, step_finish)

    def step_finish(message):
        if message.text == default_messages_user.emojicode['ok']:
            db_sess.add(user_reg)
            db_sess.commit()
            bot.send_message(message.chat.id,
                             "{0}Вы успешно заргистрированы!{0}".format(default_messages_user.emojicode['tada']),
                             reply_markup=keyboards_user.get_go_to_main_menukb())
        else:
            bot.send_message(message.chat.id, "Ничего страшного!\nМожете попробовать снова!",
                             reply_markup=keyboards_user.get_go_to_main_menukb())

    scheduleThread = Thread(target=checker)
    scheduleThread.daemon = True
    scheduleThread.start()
