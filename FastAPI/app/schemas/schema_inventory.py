"""
Schemas of Inventory
"""
from typing import Optional, Dict
from enum import Enum
from pydantic import BaseModel
from datetime import datetime, timedelta


class Item(BaseModel):
    store_name:str
    product_type: str 
    stock_level: int 

class Inventory(BaseModel):
     items: Dict[str, Item]

class StoreName(str, Enum):
     Sainsbury = "Sainsbury"
     Coop = "Coop"
     Waitrose = "Waitrose"
     Aldi = "Aldi"

item1 = Item(
    store_name="Sainsbury",
    product_type="toilet_paper",
    stock_level=3
    )

item2 = Item(
    store_name="Coop",
    product_type="soap",
    stock_level=5)

def add_datetime(inventory):
     for item_id in inventory.items:
          item_dict = inventory.items[item_id].dict()
          item_dict["datetime"] = datetime.now() - timedelta(1)
          inventory.items[item_id] = item_dict
          
inventory = Inventory(items = {"ZG011AQA":item1, "AZ246QST":item2})
add_datetime(inventory)



