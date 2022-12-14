import sqlalchemy

from .db_session import SqlAlchemyBase


class Quest(SqlAlchemyBase):
    """таблица вопросов"""
    __tablename__ = 'quests'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)  # id вопроса
    quest = sqlalchemy.Column(sqlalchemy.String(), nullable=True)  # вопрос
    chat_id = sqlalchemy.Column(sqlalchemy.String(), nullable=True)  # кто задал по chat_id
