import sqlalchemy

from .db_session import SqlAlchemyBase


class InterParty(SqlAlchemyBase):
    """таблица зареганных пользователей"""
    __tablename__ = 'InterPartis'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)  # id опросника
    date_start = sqlalchemy.Column(sqlalchemy.DateTime, nullable=True)  # дата и время начала
    comment = sqlalchemy.Column(sqlalchemy.String(), nullable=True)  # дата и время начала
    man_now = sqlalchemy.Column(sqlalchemy.Integer, nullable=True)  # человек зарегано сейчас
    man_max = sqlalchemy.Column(sqlalchemy.Integer, nullable=True)  # максимум человек
    place = sqlalchemy.Column(sqlalchemy.String(), nullable=True)  # место

