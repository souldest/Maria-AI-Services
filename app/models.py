from sqlalchemy import Column, Integer, String, Float, DateTime
from sqlalchemy.ext.declarative import declarative_base

from app.database import Base

# --- Sales Tabelle ---
class Sale(Base):
    __tablename__ = "sales"
    id = Column(Integer, primary_key=True, index=True)
    router_id = Column(Integer, nullable=False, index=True)
    amount = Column(Float, nullable=False)
    created_at = Column(DateTime, nullable=False)

# --- Inventory Tabelle ---
class Inventory(Base):
    __tablename__ = "inventory"
    id = Column(Integer, primary_key=True, index=True)
    router_id = Column(Integer, nullable=False, index=True)
    product_name = Column(String, nullable=False)
    stock_level = Column(Integer, nullable=False)
