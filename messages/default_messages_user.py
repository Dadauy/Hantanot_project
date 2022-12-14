import surrogates
from database.users_reg import UserReg
from database.inter_party import InterParty

mon = ['января', 'февраля', 'марта', "апреля", "мая", "июня", "июля", "августа", "сентября", "октября", "ноября",
       "декабря"]

# emoji
emojicode = {
    'hello': surrogates.decode('\ud83d\udc4b'),
    '1': surrogates.decode('1\ufe0f\u20e3'),
    '2': surrogates.decode('2\ufe0f\u20e3'),
    '3': surrogates.decode('3\ufe0f\u20e3'),
    '4': surrogates.decode('4\ufe0f\u20e3'),
    '5': surrogates.decode('5\ufe0f\u20e3'),
    '6': surrogates.decode('6\ufe0f\u20e3'),
    'bot': surrogates.decode('\ud83e\udd16'),
    'smile': surrogates.decode('\ud83d\ude0a'),
    'confused': surrogates.decode('\ud83d\ude23'),
    'searching': surrogates.decode('\ud83e\uddd0'),
    'fire': surrogates.decode('\ud83d\udd25'),
    'computer': surrogates.decode('\ud83d\udcbb'),
    'tada': surrogates.decode('\ud83c\udf89'),
    'kalendar': surrogates.decode('\ud83d\udcc6'),
    'pen': surrogates.decode('\u270f\ufe0f'),
    'ok': surrogates.decode('\u2705'),
    'world': surrogates.decode('\ud83c\udf10'),
    'program': surrogates.decode('\ud83d\udcd4'),
    'mic': surrogates.decode('\ud83c\udfa4'),
    'quest': surrogates.decode('\u2753'),
    'no': surrogates.decode('\u274c'),

}

HELLO_MESSAGE = "Привет!{}\nМеня зовут ITForumUgra_bot{}\nЯ телеграмбот созданный специально для ИТ-форума".format(
    emojicode['hello'], emojicode['bot'])

MAIN_MENU = [
    '1· {}О мероприятии{}'.format(emojicode['fire'], emojicode['fire']),
    '2· {}Программа мероприятия{}'.format(emojicode['program'], emojicode['program']),
    '3· {}Подписаться на оповещение о начале IT-форума{}'.format(emojicode['kalendar'], emojicode['kalendar']),
    '4· {}Задать вопрос{}'.format(emojicode['quest'], emojicode['quest']),
    '5· {}Регистрация{}'.format(emojicode['pen'], emojicode['pen']),
]


# old version == '3· {}Спикеры{}'.format(emojicode['mic'], emojicode['mic']),
def get_decription(party):
    des = "Будет проходить мероприятие под названием {}\n".format(party.name)
    des += "Немного о мероприятии:\n{}\n".format(party.comment)

    return des


def get_ivent_description(ivent):
    des = ivent.name
    des += "\n Мероприятие начинается в {}:{}".format(ivent.date_start.hour, ivent.date_start.minute)
    des += "\n Мероприятие заканчивается в {}:{}".format(ivent.date_finish.hour, ivent.date_finish.minute)
    des += "\nБудет проходить: " + ivent.place
    des += "\nНемного о мероприятии:\n" + ivent.comment
    return des


def get_data(user_reg: UserReg):
    data = "Имя: " + user_reg.name + "\n"
    data += "Фамилия: " + user_reg.surname + "\n"
    data += "Отчество: " + user_reg.patronymic + "\n"
    data += "Имя на английском: " + user_reg.name_eng + "\n"
    data += "Фамилия на английском: " + user_reg.surname_eng + "\n"
    data += "Место работы: " + user_reg.organization + "\n"
    data += "Формат участия: "
    if user_reg.format_challenge:
        data += "очно\n"
    else:
        data += "заочно\n"
    data += "СМИ: "
    if user_reg.in_smi:
        data += "ДА\n"
    else:
        data += "НЕТ\n"
    data += "Страна: " + user_reg.country + "\n"
    data += "Город: " + user_reg.city + "\n"
    data += "email: " + user_reg.email + "\n"
    data += "Номер телефона: " + user_reg.number + "\n"
    data += "Язык: " + user_reg.language + "\n"
    data += "Место работы: " + user_reg.organization + "\n"
    data += "Согласие на обработку данных:"
    if user_reg.agreement:
        data += "ДА\n"
    else:
        data += "НЕТ\n"
    print(data)

    return data


# Информация о небольших ивентах
def get_info_ivent(ivent: InterParty):
    data = ivent.comment + "\n\n"
    data += "Начало: {} {} {}:{}\n\n".format(ivent.date_start.day, mon[ivent.date_start.month - 1],
                                             ivent.date_start.hour, ivent.date_start.minute)
    data += "Сейчас зарегистрировано {} человек\n\n".format(str(ivent.man_now))
    data += "Максимальное количество мест: {}".format(str(ivent.man_max))
    return data
