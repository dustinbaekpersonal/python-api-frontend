"""
Schemas of Inventory
"""
from enum import Enum
from typing import Dict

import yaml
from pydantic import BaseModel
from utils import add_datetime

with open("../../config.yml", "r") as stream:
    config = yaml.safe_load(stream)


class Item(BaseModel):
    store_name: str
    product_type: str
    stock_level: int


class Inventory(BaseModel):
    items: Dict[str, Item]


StoreName = Enum("StoreName", {store: store for store in config["store_names"]})

item1 = Item(
    store_name=config["store_names"][0],
    product_type=config["product_types"][1],
    stock_level=config["stock_levels"][2].split(sep=',')[1],
)

item2 = Item(
    store_name=config["store_names"][1],
    product_type=config["product_types"][0],
    stock_level=config["stock_levels"][1].split(sep=',')[1],
)


inventory = Inventory(items={"ZG011AQA": item1, "AZ246QST": item2})
add_datetime(inventory)
