import telebot
from messages import default_messages_admin, keyboards_admin
import os
import openpyxl
from database import db_session
from database.programma import Programma
from database.inter_party import InterParty
import datetime


def proverka(msg):
    for c in ["КТЦ", "КВЦ", "Рестораны", "июня"]:
        if c in msg:
            return True
    return False


def test(bot, message):
    file_info = bot.get_file(message.document.file_id)
    downloaded_file = bot.download_file(file_info.file_path)
    src = os.path.abspath(message.document.file_name)
    with open(src, 'wb') as new_file:
        new_file.write(downloaded_file)
    book = openpyxl.open(src)
    sheet = book.active
    db_session.global_init("db/db_forum.db")
    db_sess = db_session.create_session()
    db_sess.query(Programma).delete()
    db_sess.query(InterParty).delete()
    db_sess.commit()
    i = 1
    while i < sheet.max_row + 1:
        if "июня" in sheet[i][0].value:
            day = int(sheet[i][0].value.split(" ")[0])
            i += 1
            while i < sheet.max_row + 1:
                if "КТЦ" in sheet[i][0].value:
                    i += 1
                    while i < sheet.max_row + 1:
                        if proverka(sheet[i][0].value):
                            break
                        st = (sheet[i][0].value).split(" – ")
                        h = int((st[0].split('.'))[0])
                        m = int((st[0].split('.'))[1])
                        h2 = int((st[1].split('.'))[0])
                        m2 = int((st[1].split('.'))[1])
                        adm = Programma(
                            name=sheet[i][1].value,
                            comment=sheet[i][2].value,
                            date_start=datetime.datetime(2023, 6, day, h, m),
                            date_finish=datetime.datetime(2023, 6, day, h2, m2),
                            place="КТЦ Югра-Классик"
                        )
                        db_sess.add(adm)
                        db_sess.commit()
                        i += 1
                elif "КВЦ" in sheet[i][0].value:
                    i += 1
                    while i < sheet.max_row + 1:
                        if proverka(sheet[i][0].value):
                            break
                        st = (sheet[i][0].value).split(" – ")
                        h = int((st[0].split('.'))[0])
                        m = int((st[0].split('.'))[1])
                        h2 = int((st[1].split('.'))[0])
                        m2 = int((st[1].split('.'))[1])
                        adm = Programma(
                            name=sheet[i][1].value,
                            comment=sheet[i][2].value,
                            date_start=datetime.datetime(2023, 6, day, h, m),
                            date_finish=datetime.datetime(2023, 6, day, h2, m2),
                            place="КВЦ Югра-Экспо"
                        )
                        db_sess.add(adm)
                        db_sess.commit()
                        i += 1
                elif "Рестораны" in sheet[i][0].value:
                    i += 1
                    while i < sheet.max_row + 1:
                        if proverka(sheet[i][0].value):
                            break
                        st = (sheet[i][0].value).split(" – ")
                        h = int((st[0].split('.'))[0])
                        m = int((st[0].split('.'))[1])
                        adm = InterParty(
                            date_start=datetime.datetime(2023, 6, day, h, m),
                            comment=sheet[i][1].value,
                            man_now=0,
                            man_max=int(sheet[i][4].value)
                        )
                        db_sess.add(adm)
                        db_sess.commit()
                        i += 1
                else:
                    break
        else:
            break


def admin(bot: telebot.TeleBot, message):
    bot.send_message(message.chat.id, default_messages_admin.HELLO_MESSAGE,
                     reply_markup=keyboards_admin.func_data())

    @bot.callback_query_handler(func=lambda call: call.data == "add")
    def excel(call):
        bot.send_message(call.message.chat.id, 'Отправьте excel файл!')

        @bot.message_handler(content_types=['document'])
        def handle_file(message):
            test(bot, message)
            bot.send_message(message.chat.id, "Все данные обновлены!!!")
