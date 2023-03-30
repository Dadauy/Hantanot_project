import telebot
from sqlalchemy.orm import Session
from database.programma_organizators import Programma_Org
from messages import default_messages_moder


def moder(bot: telebot.TeleBot, message: telebot.types.Message, db_sess: Session):
    bot.send_message(message.chat.id, "Привет", reply_markup=default_messages_moder.func_data())

    # Выбрать день
    @bot.callback_query_handler(func=lambda call: call.data == "Mprogram")
    def select_day(call):
        bot.send_message(call.message.chat.id,
                         'Программа будет проходить в течении несокльких дней\nНа какой день вы бы хотели узнать программу:',
                         reply_markup=default_messages_moder.get_daykb(db_sess.query(Programma_Org).all()))

    # Выбрать место
    @bot.callback_query_handler(func=lambda call: call.data.startswith("Mday_num"))
    def select_place(call):
        day_num = int(call.data.replace("Mday_num", ""))
        ivents: list[Programma_Org] = db_sess.query(Programma_Org).all()
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
                             reply_markup=default_messages_moder.get_places_kb(1, day_num))
        elif ucls:
            bot.send_message(call.message.chat.id, "Выберите место проведения:",
                             reply_markup=default_messages_moder.get_places_kb(2, day_num))
        elif expo:
            bot.send_message(call.message.chat.id, "Выберите место проведения:",
                             reply_markup=default_messages_moder.get_places_kb(3, day_num))

    # Выбрать зал
    @bot.callback_query_handler(func=lambda call: call.data.startswith("Mprog"))
    def select_room(call):
        type = int(call.data.replace("Mprog", "").split("*")[1])
        day = int(call.data.replace("Mprog", "").split("*")[0])
        ivents: list[Programma_Org] = db_sess.query(Programma_Org).all()

        place = ""
        if type == 1:
            place = "КТЦ"
        elif type == 2:
            place = "КВЦ"
        bot.send_message(call.message.chat.id, "Выберите зал:",
                         reply_markup=default_messages_moder.get_room_kb(place, day, ivents))

    # Отфильтрованная программа
    @bot.callback_query_handler(func=lambda call: call.data.startswith("Mallinfo"))
    def get_programm(call):
        place = call.data.replace("Mallinfo", "").split("*")[0]
        day = int(call.data.replace("Mallinfo", "").split("*")[1])
        room = call.data.replace("Mallinfo", "").split("*")[2]

        bot.send_message(call.message.chat.id, "Расписание мероприятий:")
        ivents: list[Programma_Org] = db_sess.query(Programma_Org).all()
        for ivent in ivents:
            if ivent.date_start.day == day and ivent.place.startswith(place) and ivent.place_2 == room:
                des = default_messages_moder.get_ivent_description(ivent)
                bot.send_message(call.message.chat.id, des, parse_mode="HTML")

        bot.send_message(call.message.chat.id, "Вот все мероприятия в выбранной вами локации!",
                         reply_markup=default_messages_moder.get_go_to_main_menukb())
