import sqlalchemy

from .db_session import SqlAlchemyBase


class Party(SqlAlchemyBase):
    """таблица мероприятия"""
    __tablename__ = 'partis'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)  # id мероприятия
    name = sqlalchemy.Column(sqlalchemy.String(), nullable=True)  # название мероприятия
    comment = sqlalchemy.Column(sqlalchemy.String(), nullable=True)  # о мерпориятий
