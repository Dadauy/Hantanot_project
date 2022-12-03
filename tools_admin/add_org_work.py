from database import db_session
from database.all_users import AllUsers


def add_org_work(message):
    db_session.global_init("db/db_forum.db")
    db_sess = db_session.create_session()
    org = AllUsers(
        chat_id=message.text,
        law=2
    )
    db_sess.delete(org)
    db_sess.commit()
