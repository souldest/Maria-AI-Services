from sqlalchemy import Column, Integer, String, Float, DateTime
from .database import Base

class Sale(Base):
    __tablename__ = "sales"
    id = Column(Integer, primary_key=True, index=True)
    date = Column(DateTime, nullable=False)
    product = Column(String, nullable=False)
    quantity = Column(Float, nullable=False)

class Inventory(Base):
    __tablename__ = "inventory"
    id = Column(Integer, primary_key=True, index=True)
    date = Column(DateTime, nullable=False)
    product = Column(String, nullable=False)
    stock_level = Column(Float, nullable=False)
