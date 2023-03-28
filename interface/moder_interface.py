import telebot
from messages import default_messages_user, keyboards_user
from sqlalchemy.orm import Session
from database.programma import Programma



def moder(bot: telebot.TeleBot, message: telebot.types.Message, db_sess: Session):
    # Выбрать день
    @bot.callback_query_handler(func=lambda call: call.data == "program")
    def select_day(call):
        bot.send_message(call.message.chat.id,
                         'Программа будет проходить в течении несокльких дней\nНа какой день вы бы хотели узнать программу:',
                         reply_markup=keyboards_user.get_daykb(db_sess.query(Programma).all()))

    # Выбрать место
    @bot.callback_query_handler(func=lambda call: call.data.startswith("day_num"))
    def select_place(call):
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

    # Выбрать зал
    @bot.callback_query_handler(func=lambda call: call.data.startswith("prog"))
    def select_room(call):
        type = int(call.data.replace("prog", "").split("*")[1])
        day = int(call.data.replace("prog", "").split("*")[0])
        ivents: list[Programma] = db_sess.query(Programma).all()

        place = ""
        if type == 1:
            place = "КТЦ"
        elif type == 2:
            place = "КВЦ"
        bot.send_message(call.message.chat.id, "Выберите зал:",
                         reply_markup=keyboards_user.get_room_kb(place, day, ivents))

    # Отфильтрованная программа
    @bot.callback_query_handler(func=lambda call: call.data.startswith("allinfo"))
    def get_programm(call):
        place = call.data.replace("allinfo", "").split("*")[0]
        day = int(call.data.replace("allinfo", "").split("*")[1])
        room = call.data.replace("allinfo", "").split("*")[2]

        bot.send_message(call.message.chat.id, "Расписание мероприятий:")
        ivents: list[Programma] = db_sess.query(Programma).all()
        for ivent in ivents:
            if ivent.date_start.day == day and ivent.place.startswith(place) and ivent.place_2 == room:
                des = default_messages_user.get_ivent_description(ivent)
                bot.send_message(call.message.chat.id, des, parse_mode="HTML")

        bot.send_message(call.message.chat.id, "Вот все мероприятия в выбранной вами локации!",
                         reply_markup=keyboards_user.get_go_to_main_menukb())
