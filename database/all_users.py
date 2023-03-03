import sqlalchemy

from .db_session import SqlAlchemyBase


class AllUsers(SqlAlchemyBase):
    """таблица мероприятия"""
    __tablename__ = 'all_users'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)  # id юзера
    chat_id = sqlalchemy.Column(sqlalchemy.String(), nullable=True)  # chat_id пользователя
    law = sqlalchemy.Column(sqlalchemy.Integer, nullable=True)  # уровень пользователя
    code = sqlalchemy.Column(sqlalchemy.String(), nullable=True) # код пользователя it2023#0000
