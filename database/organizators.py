import sqlalchemy

from .db_session import SqlAlchemyBase


class Moder(SqlAlchemyBase):
    """таблица организаторов"""
    __tablename__ = 'moders'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)  # id moders
    id_party = sqlalchemy.Column(sqlalchemy.Integer, nullable=True)  # id мероприятия
    name = sqlalchemy.Column(sqlalchemy.String(), nullable=True)  # ФИО
    comment = sqlalchemy.Column(sqlalchemy.String(), nullable=True)  # о модераторе
