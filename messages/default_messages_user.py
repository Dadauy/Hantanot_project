import surrogates
from database.menu_points import MenuPoint
from database.inter_party import InterParty
from messages import keyboards_user

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

HELLO_MESSAGE = "Добро пожаловать в чат-бот IT-Форума! {}{}\nВы также можете воспользоваться нашим сайтом. \nДля помощи выберите интересующий вопрос.".format(
    emojicode['hello'], emojicode['bot'])
BAGE_MESSAGE = "На стойке регистрации в КТЦ «Югра-Классик» (ул. Мира,22) с 5 по 7 июня. Рекомендуем Вам заблаговременно получить бейдж  5 июня после 16.00."
FREE_MESSAGE = "Для представителей федеральных и региональных органов власти, местного самоуправления, государственных и муниципальных учреждений, некоммерческих организаций – участие бесплатное. Для представителей коммерческих организаций  - в соответствии с партнерским пакетом."
REPORT_MESSAGE = "Необходимо до 25 мая направить тезисы доклада (примерно 1/2 машинописной страницы), указав тему, ФИО, должность и организацию на адрес (Itforum@admhmao.ru)."
CERTIFICATE_MESSAGE = "Поставить отметку можно на стойках регистрации в КТЦ «Югра-Классик» (ул. Мира,22) и КВЦ «Югра-Экспо» (ул. Студенческая, 19"


def get_decription(party):
    if party == None:
        return "GOODBYE"
    des = "Будет проходить мероприятие под названием {}\n".format(party.name)
    des += "Немного о мероприятии:\n{}\n".format(party.comment)

    return des


def get_ivent_description(ivent):
    des = "<strong>" + ivent.name + "</strong>\n"
    des += "\n<strong>Время проведения:</strong>\n{}:{} - {}:{}".format(str(ivent.date_start.hour).rjust(2, "0"),
                                                                        str(ivent.date_start.minute).rjust(2, "0"),
                                                                        str(ivent.date_finish.hour).rjust(2, "0"),
                                                                        str(ivent.date_finish.minute).rjust(2, "0"))
    des += "\n<strong>Место проведения:</strong> \n" + ivent.place
    if ivent.comment != None:
        des += "\n<strong>Немного о мероприятии:</strong>\n" + ivent.comment
    return des


# Информация о небольших ивентах
def get_info_ivent(ivent: InterParty):
    data = "<strong>" + ivent.comment + "</strong>" + "\n\n"
    data += "<strong>Начало:</strong> {} {} {}:{}\n\n".format(ivent.date_start.day, mon[ivent.date_start.month - 1],
                                                              str(ivent.date_start.hour).rjust(2, "0"),
                                                              str(ivent.date_start.minute).rjust(2, "0"))
    data += "Сейчас зарегистрировано {} человек\n\n".format(str(ivent.man_now))
    data += "Максимальное количество мест: {}".format(str(ivent.man_max))
    return data


# Формирование главного меню
def get_main_menu(menu_points: list[MenuPoint]):
    menu = ""
    cnt = 0
    for menu_point in menu_points:
        if menu_point.enable == 1:
            cnt += 1
            menu += str(cnt) + ' . {1} {0} {1} \n'.format(menu_point.text, menu_point.emoji)
    return menu, keyboards_user.get_mainkb(menu_points)
