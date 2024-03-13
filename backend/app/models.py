"""Define declarative models for ORM."""
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()


class User(Base):  # type: ignore
    """User SQLAlchemy model object."""

    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    first_name = Column(String)
    last_name = Column(String)
    email = Column(String)


class Store(Base):  # type: ignore
    """Store SQLAlchemy model object."""

    __tablename__ = "stores"

    id = Column(Integer, primary_key=True)
    store_name = Column(String, unique=True, index=True)

    products = relationship("Product", back_populates="store")


class Product(Base):  # type: ignore
    """Product SQLAlchemy model object."""

    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    product_name = Column(String, index=True)
    stock_level = Column(Integer, default=0)
    # updated_at = Column(DateTime)
    store_id = Column(Integer, ForeignKey("stores.id"), nullable=False)

    store = relationship("Store", back_populates="products")
