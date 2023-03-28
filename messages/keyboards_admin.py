from telebot import types


def func_data():
    kb = types.InlineKeyboardMarkup()
    kb.add(types.InlineKeyboardButton(text='Добавить данные для пользователя', callback_data='add'))
    kb.add(types.InlineKeyboardButton(text='Добавить данные для организатора', callback_data='add2'))
    return kb

