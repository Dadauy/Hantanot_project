from telebot import types
from messages import default_messages_user
from database import db_session
from database.programma import Programma

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

    btn = types.InlineKeyboardButton(text='Перейти в основное меню', callback_data='main_menu')

    kb.add(btn)
    return kb


# Клавиатура для основного меню
def get_mainkb():
    kb = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
    btn_list = []
    for i in range(1, 7):
        btn = types.KeyboardButton(default_messages_user.emojicode[str(i)])
        btn_list.append(btn)
    kb.row(btn_list[0], btn_list[1], btn_list[2])
    kb.row(btn_list[3], btn_list[4])

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
    kb.add(types.InlineKeyboardButton(text='Перейти в основное меню', callback_data='main_menu'))
    return kb


def get_kb_for_programma(ivent_id):
    kb = types.InlineKeyboardMarkup()
    data1 = "moder_num" + str(ivent_id)
    data2 = "speaker_num" + str(ivent_id)
    data3 = "obs_num" + str(ivent_id)

    btn1 = types.InlineKeyboardButton(text="Список организаторов", callback_data=data1)
    btn2 = types.InlineKeyboardButton(text="Список спикеров", callback_data=data2)
    btn3 = types.InlineKeyboardButton(text="Список тем, которые будут обсуждаться", callback_data=data3)
    kb.row(btn1)
    kb.row(btn2)
    kb.row(btn3)

    return kb


def get_acceptkb():
    kb = types.ReplyKeyboardMarkup(one_time_keyboard=True)
    btn1 = types.KeyboardButton(text="{}".format(default_messages_user.emojicode['ok']))
    btn2 = types.KeyboardButton(text="{}".format(default_messages_user.emojicode['no']))

    kb.row(btn1, btn2)

    return kb


def get_formatkb():
    kb = types.ReplyKeyboardMarkup(one_time_keyboard=True)
    btn1 = types.KeyboardButton(text="очно")
    btn2 = types.KeyboardButton(text="заочно")
    kb.add(btn1, btn2)

    return kb


def get_smi():
    kb = types.ReplyKeyboardMarkup(one_time_keyboard=True)
    btn1 = types.KeyboardButton(text="да")
    btn2 = types.KeyboardButton(text="нет")
    kb.add(btn1, btn2)

    return kb


def get_next():
    kb = types.ReplyKeyboardMarkup(one_time_keyboard=True)
    btn1 = types.KeyboardButton(text="Далее")
    kb.add(btn1)

    return kb


def get_other_ivents():
    kb = types.InlineKeyboardMarkup()

    btn1 = types.InlineKeyboardButton(text='Записаться на другие мероприятия', callback_data='reg_ivents')
    btn2 = types.InlineKeyboardButton(text='Перейти в основное меню', callback_data='main_menu')

    kb.row(btn1)
    kb.row(btn2)
    return kb


def get_menu_quest():
    kb = types.InlineKeyboardMarkup()
    btn1 = types.InlineKeyboardButton(text="Часто задаваемые вопросы", callback_data='bestq')
    btn2 = types.InlineKeyboardButton(text="Задать вопрос организатору", callback_data='quest')
    btn3 = types.InlineKeyboardButton(text='Перейти в основное меню', callback_data='main_menu')
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
    btn2 = types.InlineKeyboardButton(text="Перейти в основное меню", callback_data='main_menu')
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
        return kb
    elif type == 2:
        kb.add(types.InlineKeyboardButton(text="КТЦ «Югра-Классик» (ул.Мира, 22)",
               callback_data="prog" + str(day) + "*" + str(1)))
        return kb
    elif type == 3:
        kb.add(types.InlineKeyboardButton(text="КВЦ «Югра-Экспо» (ул. Студенческая, 19)",
                                          callback_data="prog" + str(day) + "*" + str(2)))
        return kb
