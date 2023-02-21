"""
Schemas of Inventory
"""
from enum import Enum
from typing import List

import yaml
from pydantic import BaseModel

with open("../config.yml", "r") as stream:
    config = yaml.safe_load(stream)

StoreName = Enum("StoreName", {store: store for store in config["stores"]})

Product = Enum("Product", {product: product for product in config["products"]})


class Item(BaseModel):
    product: Product
    store: StoreName
    stock_level: int
    datetime: str
