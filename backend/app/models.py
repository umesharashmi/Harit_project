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

class CorporateDebtMovement(Base):

    __tablename__ = "corporate_debt_movements"

    id = Column(Integer, primary_key=True, index=True)

    report_date = Column(String)

    industry_group = Column(String)

    company_name = Column(String)

    code_id = Column(String)

    debt_date = Column(String)

    coupon_rate = Column(Float)

    tom = Column(Float)

    spot = Column(Float)

    issued_date = Column(String)

    maturity_date = Column(String)

    coupon_freq = Column(Integer)

    next_interest_due_date = Column(String)

    quantity = Column(Integer)

    par = Column(Float)