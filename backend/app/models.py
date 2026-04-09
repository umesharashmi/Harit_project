from sqlalchemy import Column, String, Float
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