import telebot
from telebot import types
from messages import default_messages_user, keyboards_user
from sqlalchemy.orm import Session
from database import db_session
from database.programma import Programma
from database.inter_party import InterParty
from database.inter_party_reg import InterPartyReg
from database.all_users import AllUsers
from database.menu_points import MenuPoint
from database.menu_for_guests import MenuPointGuest


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

    menu_points: list[MenuPoint] = db_sess.query(MenuPoint).all()
    menu_points_for_guest: list[MenuPointGuest] = db_sess.query(MenuPointGuest).all()

    @bot.callback_query_handler(
        func=lambda call: call.data == 'main_menu')  # обработка кнопки перезода к основному меню
    def start_main_menu(call):  # Вывод основного меню с клавиатурой
        bot.send_message(call.message.chat.id, 'Добро Пожаловать в основное меню!')
        menu, kb = default_messages_user.get_main_menu(menu_points)
        bot.send_message(call.message.chat.id, menu, reply_markup=kb)

    # Пункт для гостей
    @bot.callback_query_handler(func=lambda call: call.data == "for_guest")
    def guest(call):
        bot.send_message(call.message.chat.id, 'Добро Пожаловать в меню для гостей!')
        menu, kb = default_messages_user.get_main_menu(menu_points_for_guest)
        kb.add(types.InlineKeyboardButton(text='Перейти в основное меню', callback_data='main_menu'))
        bot.send_message(call.message.chat.id, menu, reply_markup=kb)

    # Программа
    @bot.callback_query_handler(func=lambda call: call.data == "program")
    def program(call):
        bot.send_message(call.message.chat.id,
                         'Программа будет проходить в течении несокльких дней\nНа какой день вы бы хотели узнать программу:',
                         reply_markup=keyboards_user.get_daykb(db_sess.query(Programma).all()))

    # Задать вопрос
    @bot.callback_query_handler(func=lambda call: call.data == "ask_quest")
    def ask_quest(call):
        bot.send_message(call.message.chat.id,
                         'Вы можете отправить свой вопрос на почту Itforum@admhmao.ru, затем организаторы вам пришлют ответ!',
                         reply_markup=keyboards_user.get_go_to_main_menukb())

    # Места прведения
    @bot.callback_query_handler(func=lambda call: call.data == "place")
    def place(call):
        btn = types.InlineKeyboardButton(text="Перейти на сайт",
                                         url="https://itforum.admhmao.ru/2023/ploshchadki-foruma/")
        btn1 = types.InlineKeyboardButton(text='Перейти в основное меню', callback_data='main_menu')
        kb = types.InlineKeyboardMarkup()
        kb.add(btn1, btn)
        bot.send_message(call.message.chat.id, "Подробнее о месте проведения вы сможете узнать на сайте: ⬇️",
                         reply_markup=kb)

    # Партнёрам
    @bot.callback_query_handler(func=lambda call: call.data == "partners")
    def partners(call):
        btn = types.InlineKeyboardButton(text="Перейти на сайт",
                                         url="https://itforum.admhmao.ru/2023/partnery/")
        btn1 = types.InlineKeyboardButton(text='Перейти в основное меню', callback_data='main_menu')
        kb = types.InlineKeyboardMarkup()
        kb.add(btn1, btn)
        bot.send_message(call.message.chat.id, "Подробнее о партнёрстве вы можете узнать на сайте: ⬇️",
                         reply_markup=kb)

    # Трансфер
    @bot.callback_query_handler(func=lambda call: call.data == "car")
    def car(call):
        btn = types.InlineKeyboardButton(text="Перейти на сайт",
                                         url="https://itforum.admhmao.ru/")
        btn1 = types.InlineKeyboardButton(text='Перейти в основное меню', callback_data='main_menu')
        kb = types.InlineKeyboardMarkup()
        kb.add(btn1, btn)
        bot.send_message(call.message.chat.id, "Подробнее о трансфере вы можете узнать на сайте: ⬇️",
                         reply_markup=kb)

    # Как добраться
    @bot.callback_query_handler(func=lambda call: call.data == "get_there")
    def get_there(call):
        btn = types.InlineKeyboardButton(text="Перейти на сайт",
                                         url="https://visit-hm.ru/journals/10")
        btn1 = types.InlineKeyboardButton(text='Перейти в основное меню', callback_data='main_menu')
        kb = types.InlineKeyboardMarkup()
        kb.add(btn1, btn)
        bot.send_message(call.message.chat.id, "Подробнее вы можете узнать на этом сайте: ⬇️",
                         reply_markup=kb)

    # Где остановиться
    @bot.callback_query_handler(func=lambda call: call.data == "hotel")
    def hotel(call):
        btn = types.InlineKeyboardButton(text="Перейти на сайт",
                                         url="https://itforum.admhmao.ru/2023/gostyam/6495844-gostinitsy/")
        btn1 = types.InlineKeyboardButton(text='Перейти в основное меню', callback_data='main_menu')
        kb = types.InlineKeyboardMarkup()
        kb.add(btn1, btn)
        bot.send_message(call.message.chat.id, "Подробнее о гостиницах вы можете узнать на этом сайте: ⬇️",
                         reply_markup=kb)

    # Где поесть
    @bot.callback_query_handler(func=lambda call: call.data == "food")
    def food(call):
        btn = types.InlineKeyboardButton(text="Перейти на сайт",
                                         url="https://itforum.admhmao.ru/2023/gostyam/3353522-restorany/")
        btn1 = types.InlineKeyboardButton(text='Перейти в основное меню', callback_data='main_menu')
        kb = types.InlineKeyboardMarkup()
        kb.add(btn1, btn)
        bot.send_message(call.message.chat.id, "Подробнее о ресторанах вы можете узнать на этом сайте: ⬇️",
                         reply_markup=kb)

    # бейдж
    @bot.callback_query_handler(func=lambda call: call.data == "badge")
    def badge(call):
        btn = types.InlineKeyboardButton(text='Перейти в основное меню', callback_data='main_menu')
        kb = types.InlineKeyboardMarkup()
        kb.add(btn)
        bot.send_message(call.message.chat.id, default_messages_user.BAGE_MESSAGE,
                         reply_markup=kb)

    # Плата за участие
    @bot.callback_query_handler(func=lambda call: call.data == "participation_free")
    def participation_free(call):
        btn = types.InlineKeyboardButton(text='Перейти в основное меню', callback_data='main_menu')
        btn1 = types.InlineKeyboardButton(text='Партнёрский пакет',
                                          url="https://itforum.admhmao.ru/2023/partnery/6495838-partnerskiy-paket/")
        kb = types.InlineKeyboardMarkup()
        kb.add(btn, btn1)
        bot.send_message(call.message.chat.id, default_messages_user.FREE_MESSAGE,
                         reply_markup=kb)

    # доклад
    @bot.callback_query_handler(func=lambda call: call.data == "report")
    def report(call):
        btn = types.InlineKeyboardButton(text='Перейти в основное меню', callback_data='main_menu')
        kb = types.InlineKeyboardMarkup()
        kb.add(btn)
        bot.send_message(call.message.chat.id, default_messages_user.REPORT_MESSAGE,
                         reply_markup=kb)

    # удостоверение
    @bot.callback_query_handler(func=lambda call: call.data == "certificate")
    def certificate(call):
        btn = types.InlineKeyboardButton(text='Перейти в основное меню', callback_data='main_menu')
        kb = types.InlineKeyboardMarkup()
        kb.add(btn)
        bot.send_message(call.message.chat.id, default_messages_user.CERTIFICATE_MESSAGE,
                         reply_markup=kb)

    # что посетить в свободное время

    @bot.callback_query_handler(func=lambda call: call.data == "to_visit")
    def to_visit(call):
        btn = types.InlineKeyboardButton(text="Перейти на сайт",
                                         url="https://itforum.admhmao.ru/")
        btn1 = types.InlineKeyboardButton(text='Перейти в основное меню', callback_data='main_menu')
        kb = types.InlineKeyboardMarkup()
        kb.add(btn1, btn)
        bot.send_message(call.message.chat.id,
                         "Подробнее о том, что можно посетить на досуге вы можете узнать на сайте: ⬇️",
                         reply_markup=kb)

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
            bot.send_message(call.message.chat.id, data, reply_markup=kb, parse_mode="HTML")
            bot.send_message(call.message.chat.id, "Это всесь список экскурсий!",
                             reply_markup=keyboards_user.get_go_to_main_menukb())

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
        db_sess.add(reg)
        db_sess.commit()
        bot.send_message(call.message.chat.id,
                         "{0}Вы успешно зарегистрирваны!{0}".format(default_messages_user.emojicode["tada"]),
                         reply_markup=keyboards_user.get_other_ivents())
