import sqlalchemy

from .db_session import SqlAlchemyBase


class Work(SqlAlchemyBase):
    """таблица тематик"""
    __tablename__ = 'works'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)  # id тематики
    name = sqlalchemy.Column(sqlalchemy.String(), nullable=True)  # название тематики
