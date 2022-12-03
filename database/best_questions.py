import sqlalchemy

from .db_session import SqlAlchemyBase


class BestQuestion(SqlAlchemyBase):
    """таблица часто задаваемых вопросов"""
    __tablename__ = 'best_questions'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)  # id вопроса
    quest = sqlalchemy.Column(sqlalchemy.String(), nullable=True)  # вопрос
    response = sqlalchemy.Column(sqlalchemy.String(), nullable=True)  # ответ

