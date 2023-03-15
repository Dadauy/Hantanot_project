from telebot import types


def func_data():
    kb = types.InlineKeyboardMarkup()
    kb.add(types.InlineKeyboardButton(text='Добавить данные из excel', callback_data='add'))
    return kb
