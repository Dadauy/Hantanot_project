import sqlalchemy

from .db_session import SqlAlchemyBase


class Speaker(SqlAlchemyBase):
    """таблица спикеров"""
    __tablename__ = 'speakers'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)  # id speak
    id_party = sqlalchemy.Column(sqlalchemy.Integer, nullable=True)  # id мероприятия
    name = sqlalchemy.Column(sqlalchemy.String(), nullable=True)  # ФИО
    comment = sqlalchemy.Column(sqlalchemy.String(), nullable=True)  # о спикере
