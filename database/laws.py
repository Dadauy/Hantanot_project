import sqlalchemy

from .db_session import SqlAlchemyBase


class Laws(SqlAlchemyBase):
    """таблица прав"""
    __tablename__ = 'laws'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)  # id прав
    law = sqlalchemy.Column(sqlalchemy.String(), nullable=True)  # название прав



