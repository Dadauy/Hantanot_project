import sqlalchemy

from .db_session import SqlAlchemyBase


class ManLaw(SqlAlchemyBase):
    """таблица прав"""
    __tablename__ = 'man_laws'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)  # id пользователя с правами
    id_tg = sqlalchemy.Column(sqlalchemy.String(), nullable=True)  # id telegram
    law = sqlalchemy.Column(sqlalchemy.Integer, nullable=True)  # level law



