"""
Schemas of Inventory
"""
from typing import Optional, Dict
from enum import Enum
from pydantic import BaseModel
from utils import add_datetime


class Item(BaseModel):
    store_name:str
    product_type: str 
    stock_level: int 

class Inventory(BaseModel):
     items: Dict[str, Item]

class StoreName(str, Enum):
     Sainsbury_Euston = "Sainsbury_Euston"
     Sainsbury_Holborn = "Sainsbury_Holborn"
     Sainsbury_Soho = "Sainsbury_Soho"
     Sainsbury_Barbican = "Sainsbury_Barbican"

item1 = Item(
    store_name="Sainsbury_Euston",
    product_type="toilet_paper",
    stock_level=3
    )

item2 = Item(
    store_name="Sainsbury_Holborn",
    product_type="soap",
    stock_level=5)


inventory = Inventory(items = {"ZG011AQA":item1, "AZ246QST":item2})
add_datetime(inventory)



