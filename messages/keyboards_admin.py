from telebot import types


def data():
    kb = types.InlineKeyboardMarkup()
    kb.add(types.InlineKeyboardButton(text='Администратора', callback_data='admin'))
    kb.add(types.InlineKeyboardButton(text='Организатора', callback_data='org'))
    kb.add(types.InlineKeyboardButton(text='Частый вопрос', callback_data='quest'))

    return kb


def func_data():
    kb = types.InlineKeyboardMarkup()
    kb.add(types.InlineKeyboardButton(text='Добавить Админа/Орга/Вопрос', callback_data='add'))
    kb.add(types.InlineKeyboardButton(text='Удалить Админа/Орга/Вопрос', callback_data='delete'))
    kb.add(types.InlineKeyboardButton(text='Создать опрос', callback_data='interview'))
    return kb


def await_menu():
    kb = types.InlineKeyboardMarkup()
    btn = types.InlineKeyboardButton(text='Перейти в основное меню', callback_data='main_menu')
    kb.add(btn)
    return kb
