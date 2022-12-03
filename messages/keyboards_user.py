from telebot import types
from messages import default_messages_user


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
    kb.row(btn_list[3], btn_list[4], btn_list[5])


    return kb


# Клавиатура для инфы про спикеров
def get_speaker_infokb():
   kb = types.InlineKeyboardMarkup()

   btn1 = types.InlineKeyboardButton(text="Узнать больше", callback_data='info_speaker')
   btn2 = types.InlineKeyboardButton(text='Перейти в основное меню', callback_data='main_menu')

   kb.add(btn1).add(btn2)

   return kb




