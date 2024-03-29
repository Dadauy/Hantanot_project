import sqlalchemy

from .db_session import SqlAlchemyBase


class Programma(SqlAlchemyBase):
    """таблица мероприятия"""
    __tablename__ = 'programs'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)  # id мероприятия
    name = sqlalchemy.Column(sqlalchemy.String(), nullable=True)  # название мероприятия
    comment = sqlalchemy.Column(sqlalchemy.String(), nullable=True)  # о мерпориятий
    moder = sqlalchemy.Column(sqlalchemy.String(), nullable=True)  # модеры
    quest = sqlalchemy.Column(sqlalchemy.String(), nullable=True)  # вопросы
    date_start = sqlalchemy.Column(sqlalchemy.DateTime, nullable=True)  # начало
    date_finish = sqlalchemy.Column(sqlalchemy.DateTime, nullable=True)  # конец
    place = sqlalchemy.Column(sqlalchemy.String(), nullable=True)  # место
    place_2 = sqlalchemy.Column(sqlalchemy.String(), nullable=True)  # место_2
