from telebot import types


def get_welcomekb():
    kb = types.InlineKeyboardMarkup()
    kb.add(types.InlineKeyboardButton(text='Администратора', callback_data='admin'))
    kb.add(types.InlineKeyboardButton(text='Организатора', callback_data='org'))
    return kb


def menucb():
    kb = types.InlineKeyboardMarkup()
    btn = types.InlineKeyboardButton(text='Перейти в основное меню', callback_data='main_menu')
    kb.add(btn)
    return kb
