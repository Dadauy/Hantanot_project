from telebot import types


def data_add():
    kb = types.InlineKeyboardMarkup()
    kb.add(types.InlineKeyboardButton(text='Администратора', callback_data='admin'))
    kb.add(types.InlineKeyboardButton(text='Организатора', callback_data='org'))
    kb.add(types.InlineKeyboardButton(text='Частый вопрос', callback_data='quest'))
    kb.add(types.InlineKeyboardButton(text='Мероприятие', callback_data='program'))
    kb.add(types.InlineKeyboardButton(text='Мероприятие с регистрацией', callback_data='program'))
    return kb


def func_data():
    kb = types.InlineKeyboardMarkup()
    kb.add(types.InlineKeyboardButton(text='Добавить', callback_data='add'))
    kb.add(types.InlineKeyboardButton(text='Удалить', callback_data='delete'))
    # kb.add(types.InlineKeyboardButton(text='Изменить', callback_data='update'))
    return kb


def ways():
    kb = types.InlineKeyboardMarkup()
    kb.add(types.InlineKeyboardButton(text='Вручную', callback_data='work'))
    kb.add(types.InlineKeyboardButton(text='Из excel файла', callback_data='excel'))
    return kb
