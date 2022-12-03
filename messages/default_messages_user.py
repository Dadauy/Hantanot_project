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
    'bot':surrogates.decode('\ud83e\udd16')
}


HELLO_MESSAGE = "Привет!{}\nМеня зовут ITForumUgra_bot{}\nЯ телеграмбот созданный специально для ИТ-форума".format(emojicode['hello'], emojicode['bot'])

MAIN_MENU = [
    '1· О мероприятии',
    '2· Программа мероприятия',
    '3· Спикеры',
    '4· Подписаться на новости',
    '5· Задать вопрос',
    '6· Регистрация',
]