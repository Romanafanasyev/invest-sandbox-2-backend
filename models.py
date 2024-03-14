from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)
    balance = Column(Float, default=10000.0)
    stocks = relationship('UserStock', back_populates='user')

class Stock(Base):
    __tablename__ = 'stocks'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    price = Column(Float, nullable=False)
    quantity = Column(Integer, nullable=False)
    users = relationship('UserStock', back_populates='stock')

class UserStock(Base):
    __tablename__ = 'user_stocks'

    user_id = Column(Integer, ForeignKey('users.id'), primary_key=True)
    stock_id = Column(Integer, ForeignKey('stocks.id'), primary_key=True)
    bought_quantity = Column(Integer, nullable=False)
    user = relationship('User', back_populates='stocks')
    stock = relationship('Stock', back_populates='users')
