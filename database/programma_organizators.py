import sqlalchemy

from .db_session import SqlAlchemyBase


class Programma_Org(SqlAlchemyBase):
    """таблица мероприятия для организаторов"""
    __tablename__ = 'programs_organizators'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)  # id мероприятия
    name = sqlalchemy.Column(sqlalchemy.String(), nullable=True)  # название мероприятия
    moder = sqlalchemy.Column(sqlalchemy.String(), nullable=True)  # модеры
    numbers = sqlalchemy.Column(sqlalchemy.String(), nullable=True)  # номера телефонов
    date_start = sqlalchemy.Column(sqlalchemy.DateTime, nullable=True)  # начало
    date_finish = sqlalchemy.Column(sqlalchemy.DateTime, nullable=True)  # конец
    place = sqlalchemy.Column(sqlalchemy.String(), nullable=True)  # место
    place_2 = sqlalchemy.Column(sqlalchemy.String(), nullable=True)  # место_2
