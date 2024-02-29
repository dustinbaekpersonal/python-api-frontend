"""Schemas of Inventory."""
from enum import Enum

import yaml
from pydantic import BaseModel

with open("../config.yml", "r") as stream:
    config = yaml.safe_load(stream)

StoreName = Enum( #type: ignore
    "StoreName",
    {store: store for store in config["stores"]}
    )

Product = Enum( #type: ignore
    "Product",
    {product: product for product in config["products"]}
    )


class Item(BaseModel):
    """Pydantic BaseModel defining Item schema."""

    product: Product
    store: StoreName
    stock_level: int
    datetime: str
