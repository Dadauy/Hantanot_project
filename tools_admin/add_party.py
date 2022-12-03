import os
import openpyxl
from database import db_session
from database.all_users import AllUsers


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
        adm = AllUsers(
            chat_id=str(sheet[i][0].value),
            law=1
        )
        db_sess.add(adm)
        db_sess.commit()
