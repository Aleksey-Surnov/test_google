from app import session, Base
import sqlalchemy as db
from datetime import *
from sqlalchemy.orm import relationship, backref
from sqlalchemy import inspect
from sqlalchemy_serializer import SerializerMixin
from datetime import timedelta


class OrderInfo(Base, SerializerMixin):
    __tablename__ = 'ordersinfo'
    id = db.Column(db.Integer, primary_key = True)  # внутренний идентификатор таблицы базы.
    number_table = db.Column(db.Integer)            # идентификатор для отображения на клиенте и в БД из google.
    number_order = db.Column(db.Integer, default=0)
    date = db.Column(db.DateTime, nullable=False)
    price_usd = db.Column(db.Integer, default=0)
    price_rub = db.Column(db.Integer, default=0)


    def __init__(self, **kwargs):
        self.number_table = kwargs.get('number_table')
        self.number_order = kwargs.get('number_order')
        self.date = datetime.strptime(kwargs.get('date'), '%d.%m.%Y')
        self.price_usd = kwargs.get('price_usd')
        self.price_rub = kwargs.get('price_rub')