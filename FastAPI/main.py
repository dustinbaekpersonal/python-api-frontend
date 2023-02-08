"""
Main file for the template application
"""
from fastapi import FastAPI, Path, Query
import uvicorn
from typing import Optional, Dict
from pydantic import BaseModel
from datetime import datetime

# Initialise FastAPI App object
app = FastAPI()

class Item(BaseModel):
    datetime: datetime 
    geocode: Optional[str] = None
    input_address:Optional[str] = None
    lat:Optional[str] = None
    lng:Optional[str] = None
    product_type: str 
    resolved_address:Optional[str] = None
    stock_level: int 

class Inventory(BaseModel):
     items: Dict[int, Item]

item1 = Item(
    datetime=datetime.now(),
    geocode= "223341463921",
    input_address="WC1H 9NU",
    lat="223341",
    lng="463921",
    product_type="toilet_paper",
    resolved_address="undefined",
    stock_level=3
    )

item2 = Item(datetime=datetime.now(),
    geocode= "223341463921",
    input_address="WC1H 9NU",
    lat="223341",
    lng="463921",
    product_type="soap",
    resolved_address="undefined",
    stock_level=5)
inventory = Inventory(items = {1:item1, 2:item2})

@app.get("/")
async def root():
    return inventory.items

@app.get("/get-item/{item_id}")
async def get_stocklevel(item_id: int = Path(None, description="The ID of the item you would like to view", gt=0)):
        if item_id not in inventory.items.keys():
            return {
                "Error": "Given ID does not exist"
                }           
        return { "Product Type is": inventory.items[item_id].product_type,
                "Stock Level of" : inventory.items[item_id].stock_level
                }

@app.get("/get-by-product-type")
async def get_item(name: str = Query(None,  description="Type of item")):
        keys = [k for k,v in inventory.items.items() if v.product_type==name]
        
        return [inventory.items.get(key) for key in keys]
        # for item_id in inventory.items: ####for loop doesn't work?####
            # if inventory.items[item_id].product_type == name:
            #     return inventory.items[item_id]
            # else: 
            #     #  return {"Error":"Does not exist"}
            #      return name
        
@app.post("/create-stocklevel/{item_id}")
async def post_stocklevel(item_id: int, item: Item):
     if item_id in inventory.items.keys():
          return {"Error": "Item ID already exists"}
     inventory.items[item_id] = item
     return inventory.items[item_id]

@app.put("/update-item/{item_id}")
async def update_stocklelve(item_id: int, item: Item):
     item_dict = item.dict()
     if item_id not in inventory.items.keys():
          return {"Error": "Item ID does not exists"}
     inventory.items[item_id]=item_dict
     return inventory.items[item_id]


if __name__ == "__main__":
     uvicorn.run(app, host="0.0.0.0", port=8000)
    # for item_id in inventory.items:
    #     if inventory.items[item_id].product_type == 'soap':
    #         print(inventory.items[item_id])
    #  for item_id in inventory.items.keys():
    #       if inventory.items[item_id].product_type == 'toilet_paper':
    #         print(item_id)
    #  if 1 in inventory.items.keys():
    #     print('yep')
    #     print(inventory.items[1].geocode)
    #  else:
    #     print(inventory.items.keys())
    # # main()