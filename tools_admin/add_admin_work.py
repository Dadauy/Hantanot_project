from database import db_session
from database.all_users import AllUsers


def add_admin_work(message):
    db_session.global_init("db/db_forum.db")
    db_sess = db_session.create_session()
    adm = AllUsers(
        chat_id=message.text,
        law=1
    )
    db_sess.add(adm)
    db_sess.commit()
