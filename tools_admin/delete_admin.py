from database import db_session
from database.all_users import AllUsers


def delete_admin(message):
    db_session.global_init("db/db_forum.db")
    db_sess = db_session.create_session()
    adm = db_sess.query(AllUsers).filter(AllUsers.chat_id == message.chat.id).first()
    db_sess.delete(adm)
    db_sess.commit()
