from telebot import types
from messages import default_messages_user
from database import db_session
from database.programma import Programma
from database.menu_points import MenuPoint


def get_ivent_description(ivent: Programma):
    des = "<strong>" + ivent.name + "</strong>\n"
    des += "\n<strong>Время проведения:</strong>\n{}:{} - {}:{}".format(str(ivent.date_start.hour).rjust(2, "0"),
                                                                        str(ivent.date_start.minute).rjust(2, "0"),
                                                                        str(ivent.date_finish.hour).rjust(2, "0"),
                                                                        str(ivent.date_finish.minute).rjust(2, "0"))
    moders = []
    numbers = []
    des += "\n<strong>Выступающие: </strong> \n"
    if ivent.moder != None:
        for moder in ivent.moder.split("#"):
            moders.append(moder)
    if ivent.numbers != None:
        for number in ivent.numbers.split("#"):
            numbers.append(number)
    for i in range(len(moders)):
        des += f"{moders[i]}: {numbers[i]}\n"
    return des


def func_data():
    kb = types.InlineKeyboardMarkup()
    kb.add(types.InlineKeyboardButton(text='выбрать день', callback_data='program'))
    return kb


mon = ['января', 'февраля', 'марта', "апреля", "мая", "июня", "июля", "августа", "сентября", "октября", "ноября",
       "декабря"]


# Клавиатура для приветствия
def get_welcomekb():
    kb = types.InlineKeyboardMarkup()

    btn = types.InlineKeyboardButton(text='Узнать больше', callback_data='about')

    kb.add(btn)
    return kb


# клавиатура для перехода к основному меню
def get_go_to_main_menukb():
    kb = types.InlineKeyboardMarkup()

    btn = types.InlineKeyboardButton(text='Перейти в основное меню', callback_data='program')

    kb.add(btn)
    return kb


# Клавиатура для основного меню
def get_mainkb(menu_points: list[MenuPoint]):
    kb = types.InlineKeyboardMarkup()
    cnt = 0
    k = 0
    btnlst = []
    for menu_point in menu_points:
        if menu_point.enable == 1:
            cnt += 1
            k += 1
            if menu_point.url == None:
                btn = types.InlineKeyboardButton(text=str(cnt) + ". " + menu_point.emoji,
                                                 callback_data=menu_point.callback_data)
            else:
                btn = types.InlineKeyboardButton(text=str(cnt) + ". " + menu_point.emoji,
                                                 url=menu_point.url)
            btnlst.append(btn)
            if k == 3:
                kb.add(btnlst[0], btnlst[1], btnlst[2])
                k = 0
                btnlst.clear()
    if k == 1:
        kb.add(btnlst[0])
        btnlst.clear()
    elif k == 2:
        kb.add(btnlst[0], btnlst[1])
        btnlst.clear()
    return kb


# Клавиатура для дней
def get_daykb(programma: list[Programma]):
    kb = types.InlineKeyboardMarkup()
    month = programma[0].date_start.month
    monthst = mon[int(month) - 1]
    days = set()
    for ivent in programma:
        days.add(ivent.date_start.day)
    dayl = sorted([i for i in days])

    for day in dayl:
        text = str(day) + " " + monthst
        data = "day_num" + str(day)
        btn = types.InlineKeyboardButton(text=text, callback_data=data)
        kb.add(btn)
    kb.add(types.InlineKeyboardButton(text='Перейти в основное меню', callback_data='program'))
    return kb


def get_acceptkb():
    kb = types.ReplyKeyboardMarkup(one_time_keyboard=True)
    btn1 = types.KeyboardButton(text="{}".format(default_messages_user.emojicode['ok']))
    btn2 = types.KeyboardButton(text="{}".format(default_messages_user.emojicode['no']))

    kb.row(btn1, btn2)

    return kb


def get_next():
    kb = types.ReplyKeyboardMarkup(one_time_keyboard=True)
    btn1 = types.KeyboardButton(text="Далее")
    kb.add(btn1)

    return kb


def get_other_ivents():
    kb = types.InlineKeyboardMarkup()

    btn1 = types.InlineKeyboardButton(text='Список экскурсий', callback_data='reg_ivents')
    btn2 = types.InlineKeyboardButton(text='Перейти в основное меню', callback_data='program')

    kb.row(btn1)
    kb.row(btn2)
    return kb


def get_menu_quest():
    kb = types.InlineKeyboardMarkup()
    btn1 = types.InlineKeyboardButton(text="Часто задаваемые вопросы", callback_data='bestq')
    btn2 = types.InlineKeyboardButton(text="Задать вопрос организатору", callback_data='quest')
    btn3 = types.InlineKeyboardButton(text='Перейти в основное меню', callback_data='program')
    kb.row(btn1)
    kb.row(btn2)
    kb.row(btn3)

    return kb


def get_go_to_main_site():
    kb = types.InlineKeyboardMarkup()
    btn1 = types.InlineKeyboardButton(text="Перейти на сайт IT форума", url="https://itforum.admhmao.ru/")
    kb.add(btn1)
    return kb


def get_go_to_main_site_and_main_menu():
    kb = types.InlineKeyboardMarkup()
    btn1 = types.InlineKeyboardButton(text="Перейти на сайт IT форума", url="https://itforum.admhmao.ru/")
    btn2 = types.InlineKeyboardButton(text="Перейти в основное меню", callback_data='program')
    kb.add(btn1)
    kb.add(btn2)
    return kb


def get_places_kb(type: int, day: int):
    # type 1 full, type 2 ucls, type 3
    kb = types.InlineKeyboardMarkup()
    if type == 1:
        kb.add(types.InlineKeyboardButton(text="КТЦ «Югра-Классик» (ул.Мира, 22)",
                                          callback_data="prog" + str(day) + "*" + str(1)))
        kb.add(types.InlineKeyboardButton(text="КВЦ «Югра-Экспо» (ул. Студенческая, 19)",
                                          callback_data="prog" + str(day) + "*" + str(2)))
        kb.add(types.InlineKeyboardButton(text='Перейти в основное меню', callback_data='program'))
        return kb
    elif type == 2:
        kb.add(types.InlineKeyboardButton(text="КТЦ «Югра-Классик» (ул.Мира, 22)",
                                          callback_data="prog" + str(day) + "*" + str(1)))
        kb.add(types.InlineKeyboardButton(text='Перейти в основное меню', callback_data='program'))
        return kb
    elif type == 3:
        kb.add(types.InlineKeyboardButton(text="КВЦ «Югра-Экспо» (ул. Студенческая, 19)",
                                          callback_data="prog" + str(day) + "*" + str(2)))
        kb.add(types.InlineKeyboardButton(text='Перейти в основное меню', callback_data='program'))
        return kb


def get_room_kb(place: str, day: int, ivents: list[Programma]):
    kb = types.InlineKeyboardMarkup()
    rooms = set()
    for ivent in ivents:
        if ivent.place.startswith(place) and ivent.date_start.day == day:
            rooms.add(ivent.place_2)
    for room in rooms:
        btn = types.InlineKeyboardButton(text=room, callback_data='allinfo' + place + '*' + str(day) + "*" + room)
        kb.add(btn)
    return kb
