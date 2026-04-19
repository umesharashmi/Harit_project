from sqlalchemy import Column, String, Float,Integer
from .database import Base

class Price(Base):
    __tablename__ = "prices"

    id = Column(String, primary_key=True)
    date = Column(String)
    city = Column(String)
    item = Column(String)
    category = Column(String)
    min_price = Column(Float)
    max_price = Column(Float)

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    password = Column(String)
    role = Column(String)  # "view" or "download"