import os
import openpyxl
from database import db_session
from database.programma import Programma
from database.speakers import Speaker
from database.organizators import Moder
from database.temas import Tema


def add_party(bot, message):
    file_info = bot.get_file(message.document.file_id)
    downloaded_file = bot.download_file(file_info.file_path)
    src = os.path.abspath(message.document.file_name)
    with open(src, 'wb') as new_file:
        new_file.write(downloaded_file)
    book = openpyxl.open(src)
    sheet = book.active
    db_session.global_init("db/db_forum.db")
    db_sess = db_session.create_session()
    for i in range(1, sheet.max_row + 1):
        prog = Programma()
        for j in range(0, 10):
            if j == 0:
                prog.name = sheet[i][j].value
            elif j == 1:
                prog.comment = sheet[i][j].value
            elif j == 2:
                prog.date_start = sheet[i][j].value
            elif j == 3:
                prog.date_finish = sheet[i][j].value
            elif j == 4:
                prog.place = sheet[i][j].value
                db_sess.add(prog)
                db_sess.commit()
            elif j == 5:
                res = db_sess.query(Programma).filter(Programma.name == sheet[i][0].value).first()
                names = sheet[i][j].value.split("#")
                comments = sheet[i][j + 1].value.split("#")
                for k in range(len(names)):
                    speaker = Speaker(
                        id_party=res.id,
                        name=names[k],
                        comment=comments[k]
                    )
                    db_sess.add(speaker)
                    db_sess.commit()
            elif j == 7:
                res = db_sess.query(Programma).filter(Programma.name == sheet[i][0].value).first()
                names = sheet[i][j].value.split("#")
                comments = sheet[i][j + 1].value.split("#")
                for k in range(len(names)):
                    moder = Moder(
                        id_party=res.id,
                        name=names[k],
                        comment=comments[k]
                    )
                    db_sess.add(moder)
                    db_sess.commit()
            elif j == 9:
                res = db_sess.query(Programma).filter(Programma.name == sheet[i][0].value).first()
                comments = sheet[i][j].value.split("#")
                for comment in comments:
                    tema = Tema(
                        id_party=res.id,
                        comment=comment
                    )
                    db_sess.add(tema)
                    db_sess.commit()
