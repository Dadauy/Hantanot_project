import sqlalchemy

from .db_session import SqlAlchemyBase


class MenuPoint(SqlAlchemyBase):
    """таблица для пунктов меню"""
    __tablename__ = 'menu_points'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)  # id пункта
    text = sqlalchemy.Column(sqlalchemy.String(), nullable=True)  # текст пункта
    enable = sqlalchemy.Column(sqlalchemy.Boolean, nullable=True)  # активен/неактивен
    emoji = sqlalchemy.Column(sqlalchemy.String(), nullable=True)  # emoji для пункта
    callback_data = sqlalchemy.Column(sqlalchemy.String(), nullable=True) # callback data for inline button
