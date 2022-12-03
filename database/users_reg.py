import sqlalchemy

from .db_session import SqlAlchemyBase


class UserReg(SqlAlchemyBase):
    """таблица зареганных пользователей"""
    __tablename__ = 'users_reg'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)  # id пользователя
    id_tg = sqlalchemy.Column(sqlalchemy.String(), nullable=True)  # chatid юзера
    name = sqlalchemy.Column(sqlalchemy.String(), nullable=True)  # имя
    surname = sqlalchemy.Column(sqlalchemy.String(), nullable=True)  # фамилия
    patronymic = sqlalchemy.Column(sqlalchemy.String(), nullable=True)  # отчество
    name_eng = sqlalchemy.Column(sqlalchemy.String(), nullable=True)  # имя на англиском
    surname_eng = sqlalchemy.Column(sqlalchemy.String(), nullable=True)  # фамилия на англиском
    id_work = sqlalchemy.Column(sqlalchemy.Integer, nullable=True)  # id работы
    organization = sqlalchemy.Column(sqlalchemy.String(), nullable=True)  # имя организации
    format_challenge = sqlalchemy.Column(sqlalchemy.Boolean, nullable=True)  # очно или заочно
    in_smi = sqlalchemy.Column(sqlalchemy.Boolean, nullable=True)  # в СМИ? да/нет
    country = sqlalchemy.Column(sqlalchemy.String(), nullable=True)  # страна
    city = sqlalchemy.Column(sqlalchemy.String(), nullable=True)  # город
    email = sqlalchemy.Column(sqlalchemy.String(), nullable=True)  # email
    number = sqlalchemy.Column(sqlalchemy.String(), nullable=True)  # номер телефона
    language = sqlalchemy.Column(sqlalchemy.String(), nullable=True)  # номер телефона
    agreement = sqlalchemy.Column(sqlalchemy.Boolean, nullable=True)  # согласие на обработку ПД


