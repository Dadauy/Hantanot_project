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
def get_daykb(programma):
    kb = types.InlineKeyboardMarkup()
    month = programma[0].date_start.month
    months = mon[int(month) - 1]
    days = set()
    for ivent in programma:
        days.add(ivent.date_start.day)
    dayl = sorted([i for i in days])

    for day in dayl:
        text = str(day) + " " + months
        data = "day_num" + str(day)
        btn = types.InlineKeyboardButton(text=text, callback_data=data)
        kb.add(btn)
    kb.add(types.InlineKeyboardButton(text='Перейти в основное меню', callback_data='main_menu'))
    return kb

def get_kb_for_programma(ivent_id):
    kb = types.InlineKeyboardMarkup()
    data1 = "moder_num:" + str(ivent_id)
    data2 = "speaker_num:" + str(ivent_id)
    data3 = "obs_num:" + str(ivent_id)

    btn1 = types.InlineKeyboardButton(text="Список модераторов", callback_data=data1)
    btn2 = types.InlineKeyboardButton(text="Список спикеров", callback_data=data2)
    btn3 = types.InlineKeyboardButton(text="Список тем, которые будут обсуждаться", callback_data=data3)
    kb.row(btn1)
    kb.row(btn2)
    kb.row(btn3)

    return kb

