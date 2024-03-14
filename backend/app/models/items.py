"""Declarative ORM models for inventory."""
from sqlalchemy import ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base


class Store(Base):  # type: ignore
    """Store orm model class.

    Attributes:
        id (int): unique ID assigned for each store
        store_name (str): name of stores e.g. Waitrose, Sainsbury's
        products (Product): associated Product class

    Methods:
        __repr__: to print out Store class with attributes
    """

    __tablename__ = "stores"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    store_name: Mapped[str] = mapped_column(String, nullable=False, unique=True, index=True)

    products: Mapped["Product"] = relationship(back_populates="store")

    def __repr__(self) -> str:
        """Returns string representation of class."""
        return f"Store detail: ID={self.id}, Store Name={self.store_name}"


class Product(Base):  # type: ignore
    """Product orm model class.

    Attributes:
        id (int): unique ID assigned for each product
        product_name (str): name of products e.g. milk, bread
        stock_level (int): current number of products in given store
        store_id (int): foreign key to id of Store class
        store (Store): associated Store class

    Methods:
        __repr__: to print out Product class with attributes
    """

    __tablename__ = "products"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    product_name: Mapped[str] = mapped_column(String, nullable=False, index=True)
    stock_level: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    store_id: Mapped[int] = mapped_column(Integer, ForeignKey("stores.id"), nullable=False)

    store = relationship("Store", back_populates="products")

    def __repr__(self) -> str:
        """Return string representation of class."""
        return (
            f"Product detail: ID={self.id}, Product Name={self.product_name} \n"
            + f"Stock Level={self.stock_level} in Store ID={self.store_id}"
        )
