from telebot import types
import default_messages


def get_welcomekb():
    kb = types.InlineKeyboardMarkup()

    btn = types.InlineKeyboardButton(text='Узнать больше', callback_data='about')

    kb.add(btn)
    return kb

def get_go_to_main_menukb():
    kb = types.InlineKeyboardMarkup()

    btn = types.InlineKeyboardButton(text='Основное меню', callback_data='main_menu')

    kb.add(btn)
    return kb

def get_mainkb():
    kb = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)

    for i in range(1,7):
        btn = types.KeyboardButton(default_messages.emojicode[str(i)])
        kb.add(btn)
    return kb