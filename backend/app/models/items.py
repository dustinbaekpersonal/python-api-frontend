"""Declarative ORM models for inventory."""
from fastapi import HTTPException
from sqlalchemy import ForeignKey, Integer, String, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base


class Store(Base):
    """Store orm model class.

    Attributes:
        id (int): unique ID assigned for each store
        store_name (str): name of stores e.g. Waitrose, Sainsbury's
        products (Product): associated Product class

    Methods:
        __repr__: to print out Store class with attributes
        search: find a store by store_name
    """

    __tablename__ = "stores"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    store_name: Mapped[str] = mapped_column(String, nullable=False, unique=True, index=True)

    products: Mapped["Product"] = relationship(back_populates="store")

    def __repr__(self) -> str:
        """Returns string representation of class."""
        return f"Store detail: ID={self.id}, Store Name={self.store_name}"

    @classmethod
    async def search(cls, store_name: str, db: AsyncSession):
        """Class method to find a store using store name."""
        statement = select(cls).where(cls.store_name == store_name)
        result = await db.execute(statement)
        result = result.scalars().first()
        if not result:
            raise HTTPException(status_code=404, detail=f"Store '{store_name}' not found.")
        return result


class Product(Base):
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

    @classmethod
    async def search_by_store(cls, store_id: int, db: AsyncSession):
        """Class method to find a products by store_id."""
        statement = select(cls).where(cls.store_id == store_id)
        result = await db.execute(statement)
        result = result.scalars().all()

        if not result:
            raise HTTPException(
                status_code=404,
                detail=f"Store {cls.store_name} does not have any inventory.",
            )

        return result

    @classmethod
    async def search_by_store_product_name(
        cls, store_id: int, product_name: str, db: AsyncSession
    ):
        """Finds a product detail for given store id and product name."""
        statement = select(cls).where(
            cls.store_id == store_id,
            cls.product_name == product_name,
        )
        result = await db.execute(statement)
        result = result.scalars().first()

        if not result:
            raise HTTPException(
                status_code=404,
                detail=f"Store ID {cls.id} does not have product {product_name}",
            )
        return result
