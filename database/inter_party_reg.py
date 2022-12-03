import sqlalchemy

from .db_session import SqlAlchemyBase


class InterPartyReg(SqlAlchemyBase):
    """таблица зареганных пользователей"""
    __tablename__ = 'inter_party_reg'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)  # id party reg
    id_party = sqlalchemy.Column(sqlalchemy.Integer, nullable=True)  # id party
    chatid = sqlalchemy.Column(sqlalchemy.String(), nullable=True)  # chatid
