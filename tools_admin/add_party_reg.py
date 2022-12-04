import os
import openpyxl
from database import db_session
from database.inter_party import InterParty


def add_party_reg(bot, message):
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
        party_reg = InterParty()
        for j in range(0, 4):
            if j == 0:
                party_reg.date_start = sheet[i][j].value
            elif j == 1:
                party_reg.comment = sheet[i][j].value
            elif j == 2:
                party_reg.man_max = sheet[i][j].value
            elif j == 3:
                party_reg.man_now = 0
                db_sess.add(party_reg)
                db_sess.commit()
