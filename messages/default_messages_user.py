import surrogates

#emoji
emojicode = {
    'hello': surrogates.decode('\ud83d\udc4b'),
    '1':surrogates.decode('1\ufe0f\u20e3'),
    '2':surrogates.decode('2\ufe0f\u20e3'),
    '3':surrogates.decode('3\ufe0f\u20e3'),
    '4':surrogates.decode('4\ufe0f\u20e3'),
    '5':surrogates.decode('5\ufe0f\u20e3'),
    '6':surrogates.decode('6\ufe0f\u20e3'),
    'bot':surrogates.decode('\ud83e\udd16'),
    'smile':surrogates.decode('\ud83d\ude0a'),
    'confused':surrogates.decode('\ud83d\ude23'),
    'searching':surrogates.decode('\ud83e\uddd0'),
    'fire':surrogates.decode('\ud83d\udd25'),
    'computer':surrogates.decode('\ud83d\udcbb'),
    'tada':surrogates.decode('\ud83c\udf89'),
    'kalendar':surrogates.decode('\ud83d\udcc6'),
    'pen':surrogates.decode('\u270f\ufe0f'),
    'ok':surrogates.decode('\u2705'),
    'world':surrogates.decode('\ud83c\udf10'),
    'program':surrogates.decode('\ud83d\udcd4'),
    'mic':surrogates.decode('\ud83c\udfa4'),
    'quest':surrogates.decode('\u2753'),



}


HELLO_MESSAGE = "Привет!{}\nМеня зовут ITForumUgra_bot{}\nЯ телеграмбот созданный специально для ИТ-форума".format(emojicode['hello'], emojicode['bot'])

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
