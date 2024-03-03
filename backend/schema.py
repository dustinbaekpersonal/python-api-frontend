"""Schemas of Inventory."""
from datetime import datetime
from typing import List

from pydantic import BaseModel


class ProductNames(BaseModel):
    """Pydantic model for products."""

    product_name: str
    stock_level: int
    created_date: datetime


class Inventory(BaseModel):
    """Pydantic model for stores."""

    store_name: str
    product_name: List[ProductNames]
