import sqlalchemy

from .db_session import SqlAlchemyBase


class Tema(SqlAlchemyBase):
    """таблица тем"""
    __tablename__ = 'temas'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)  # id темы
    id_party = sqlalchemy.Column(sqlalchemy.Integer, nullable=True)  # id мероприятия
    comment = sqlalchemy.Column(sqlalchemy.String(), nullable=True)  # темы
