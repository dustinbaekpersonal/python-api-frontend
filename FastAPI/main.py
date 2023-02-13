"""
Main file for the template application
"""
from fastapi import FastAPI, Path, Query, HTTPException
from enum import Enum
import uvicorn
from typing import Optional, Dict
from pydantic import BaseModel
from datetime import datetime, timedelta

# Initialise FastAPI App object
app = FastAPI()

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


@app.get("/")
async def all_stocklevels():
    return inventory.items

@app.get("/store_names/{store_name}")
async def get_store_name(store_name: StoreName):
     keys = [k for k,v in inventory.items.items() if v["store_name"]==store_name]
     if keys:
          return {"Store_name": store_name}
     raise HTTPException(status_code=404, detail="Store not found")

@app.get("/get-item/{item_id}") 
async def get_stocklevel(item_id: str = Path(None, description="The ID of the item you would like to view")):
        if item_id not in inventory.items.keys():
          raise HTTPException(status_code=404, detail="Given ID does not exist")
       
        return { "Store Name is ": inventory.items[item_id]["store_name"],
             "Product Type is": inventory.items[item_id]["product_type"],
                "Stock Level of" : inventory.items[item_id]["stock_level"],
                "Datetime": inventory.items[item_id]["datetime"]
                }

@app.get("/get-by-store-and-product-name")
async def get_item_by_store(store_name: StoreName, name: str = Query(None,  description="Type of item")):
     keys = [k for k,v in inventory.items.items() if v["store_name"]==store_name and v["product_type"]==name]
     if keys:
          return [inventory.items.get(key) for key in keys]
     raise HTTPException(status_code=404, detail=f"{store_name} does not have any stock of {name}")

        
@app.post("/create-stocklevel/{item_id}")
async def post_stocklevel(item_id: str, item: Item):
     item_dict = item.dict()
     if item_id in inventory.items.keys():
          raise HTTPException(status_code=404, detail="Item ID already exists")
     item_dict["datetime"] = datetime.now()
     inventory.items[item_id] = item_dict

     return inventory.items[item_id]

@app.put("/update-item/{item_id}")
async def update_stocklevel(item_id: str, item: Item):
     item_dict = item.dict()
     if item_id not in inventory.items.keys():
          raise HTTPException(status_code=404, detail="Item ID does not exists")
     item_dict["datetime"] = datetime.now()
     inventory.items[item_id]=item_dict
     return inventory.items[item_id]


if __name__ == "__main__":
     uvicorn.run(app, host="0.0.0.0", port=8000)