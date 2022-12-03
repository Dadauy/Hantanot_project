import sqlalchemy

from .db_session import SqlAlchemyBase


class Programma(SqlAlchemyBase):
    """таблица мероприятия"""
    __tablename__ = 'programs'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)  # id мероприятия
    name = sqlalchemy.Column(sqlalchemy.String(), nullable=True)  # название мероприятия
    comment = sqlalchemy.Column(sqlalchemy.String(), nullable=True)  # о мерпориятий
    date_start = sqlalchemy.Column(sqlalchemy.DateTime, nullable=True)  # начало
    date_finish = sqlalchemy.Column(sqlalchemy.DateTime, nullable=True)  # конец
    place = sqlalchemy.Column(sqlalchemy.String(), nullable=True)  # место
    speakers = sqlalchemy.Column(sqlalchemy.String(), nullable=True)  # спикеры
    moders = sqlalchemy.Column(sqlalchemy.String(), nullable=True)  # можераторы
    temaobs = sqlalchemy.Column(sqlalchemy.String(), nullable=True)  # темы для обсуждения
