"""Schemas of Inventory."""
from datetime import datetime
from enum import Enum
from typing import List

from pydantic import BaseModel


class AllowedStoreNames(str, Enum):
    """Allowed store names."""

    waitrose = "Waitrose"
    sainsbury = "Sainsbury's"
    aldi = "Aldi"


class AllowedProductNames(str, Enum):
    """Allowed product names."""

    milk = "milk"
    bread = "bread"
    fruit = "fruit"


class ProductNames(BaseModel):
    """Pydantic model for products."""

    product_name: AllowedProductNames
    stock_level: int
    updated_date: datetime


class Inventory(BaseModel):
    """Pydantic model for stores."""

    store_name: AllowedStoreNames
    product_name: List[ProductNames]
