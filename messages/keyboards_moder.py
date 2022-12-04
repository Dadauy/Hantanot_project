from telebot import types


def yes_or_no():
    kb = types.InlineKeyboardMarkup()
    kb.add(types.InlineKeyboardButton(text='Посмотреть', callback_data='yes'))
    return kb


def answer():
    kb = types.InlineKeyboardMarkup()
    kb.add(types.InlineKeyboardButton(text='Ответить', callback_data='answer'))
    return kb
