"""Define declarative models for ORM."""
from datetime import datetime

from database import Base
from sqlalchemy import Column, DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import relationship


class Store(Base):
    """Store SQLAlchemy model object."""

    __tablename__ = "stores"

    id = Column(Integer, primary_key=True)
    store_name = Column(String, unique=True, index=True)

    products = relationship("Product", back_populates="store")


class Product(Base):
    """Product SQLAlchemy model object."""

    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    product_name = Column(String, index=True)
    stock_level = Column(Integer, default=0)
    created_date = Column(DateTime, default=datetime.utcnow)
    store_id = Column(Integer, ForeignKey("stores.id"), nullable=False)

    store = relationship("Store", back_populates="products")
