"""Schemas of Inventory."""
from enum import Enum

from pydantic import BaseModel

config = {
    "products": ["milk", "bread", "fruit", "vegetables"],
    "stores": [
        "Sainsbury's Euston",
        "Sainsbury's Holborn",
        "Sainsbury's Soho",
        "Sainsbury's Barbican",
    ],
}

StoreName = Enum(  # type: ignore
    "StoreName", {store: store for store in config["stores"]}
)

Product = Enum(  # type: ignore
    "Product", {product: product for product in config["products"]}
)


class Item(BaseModel):
    """Pydantic BaseModel defining Item schema."""

    product: Product
    store: StoreName
    stock_level: int
    datetime: str
