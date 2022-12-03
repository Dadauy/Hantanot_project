import sqlalchemy

from .db_session import SqlAlchemyBase


class Speaker(SqlAlchemyBase):
    """таблица спикера"""
    __tablename__ = 'speakers'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)  # id спикера
    name = sqlalchemy.Column(sqlalchemy.String(), nullable=True)  # имя спикера
    surname = sqlalchemy.Column(sqlalchemy.String(), nullable=True)  # фамилия спикера
    patronymic = sqlalchemy.Column(sqlalchemy.String(), nullable=True)  # отчество спикера
    work = sqlalchemy.Column(sqlalchemy.Integer, nullable=True)  # работа спикера
    comment = sqlalchemy.Column(sqlalchemy.String(), nullable=True)  # дополнительная информация про спикера
