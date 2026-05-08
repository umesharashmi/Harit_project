from sqlalchemy import Column, String, Float,Integer,Date
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


class CountryArrival(Base):
    __tablename__ = "country_arrivals"

    id = Column(String, primary_key=True)
    country = Column(String)
    year = Column(Integer)

    jan = Column(Integer)
    feb = Column(Integer)
    mar = Column(Integer)
    apr = Column(Integer)
    may = Column(Integer)
    jun = Column(Integer)
    jul = Column(Integer)
    aug = Column(Integer)
    sep = Column(Integer)
    oct = Column(Integer)
    nov = Column(Integer)
    dec = Column(Integer)

    total = Column(Integer)

class EquityMovement(Base):

    __tablename__ = "equity_movements"

    id = Column(Integer, primary_key=True, index=True)

    report_date = Column(String)
    industry_group = Column(String)
    board = Column(String)
    company_name = Column(String)
    type = Column(String)
    close_price = Column(Float)
    last_traded_price = Column(Float)
    last_traded_date = Column(String)
    high = Column(Float)
    low = Column(Float)
    foreign_holding = Column(Integer)
    turnover = Column(Float)
    quantity = Column(Integer)