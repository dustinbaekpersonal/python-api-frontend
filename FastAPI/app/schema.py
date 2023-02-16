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
     Sainsbury_Euston = "Sainsburys_Euston"
     Sainsbury_Holborn = "Sainsburys_Holborn"
     Sainsbury_Soho = "Sainsburys_Soho"
     Sainsbury_Barbican = "Sainsburys_Barbican"

item1 = Item(
    store_name="Sainsburys_Euston",
    product_type="toilet_paper",
    stock_level=3
    )

item2 = Item(
    store_name="Sainsburys_Holborn",
    product_type="soap",
    stock_level=5)


inventory = Inventory(items = {"ZG011AQA":item1, "AZ246QST":item2})
add_datetime(inventory)



