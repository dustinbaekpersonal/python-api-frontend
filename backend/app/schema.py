"""Schemas of Inventory."""
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

class UserDetails(BaseModel):
    """Pydantic model for users."""
    first_name: str
    last_name: str
    email: str

class ProductNames(BaseModel):
    """Pydantic model for products."""

    product_name: AllowedProductNames
    stock_level: int
    # updated_at: datetime


class Inventory(BaseModel):
    """Pydantic model for stores."""

    store_name: AllowedStoreNames
    product_detail: List[ProductNames]
