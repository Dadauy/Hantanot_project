from database import db_session
from database.best_questions import BestQuestion


def delete_quest(message):
    db_session.global_init("db/db_forum.db")
    db_sess = db_session.create_session()
    q_ans_r = message.text.split("#")
    best_quest = db_sess.query(BestQuestion).filter(
        BestQuestion.quest == q_ans_r[0] and BestQuestion.response == q_ans_r[1]).first()
    db_sess.delete(best_quest)
    db_sess.commit()
