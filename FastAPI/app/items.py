from fastapi import APIRouter, Path, Query, HTTPException
from datetime import datetime
from schema import inventory, StoreName, Item
from utils import submit_stocklevel

router = APIRouter()

initial_stock_to_csv=list(map(lambda x: submit_stocklevel(inventory.items[x]), inventory.items))

@router.get("/stock")
async def all_stocklevels():
    return inventory.items

# @router.get("/store_names/{store_name}")
# async def get_store_name(store_name: StoreName):
#      keys = [k for k,v in inventory.items.items() if v["store_name"]==store_name]
#      if keys:
#           return {"Store_name": store_name}
#      raise HTTPException(status_code=404, detail="Store not found")

@router.get("/get-item/{item_id}") 
async def get_stocklevel(item_id: str = Path(None, description="The ID of the item you would like to view")):
        if item_id not in inventory.items.keys():
          raise HTTPException(status_code=404, detail="Given ID does not exist")
       
        return { "Store Name is ": inventory.items[item_id]["store_name"],
             "Product Type is": inventory.items[item_id]["product_type"],
                "Stock Level of" : inventory.items[item_id]["stock_level"],
                "Datetime": inventory.items[item_id]["datetime"]
                }

@router.get("/get-by-product-name")
async def get_item_by_product_name(product_type: str = Query(None,  description="Type of item")):
     keys = [k for k,v in inventory.items.items() if v["product_type"]==product_type]
     if keys:
          return [inventory.items.get(key) for key in keys]
     raise HTTPException(status_code=404, detail=f"All four stores do not have any stock of {product_type}")


@router.get("/get-by-store-and-product-name")
async def get_item_by_store(store_name: StoreName, product_type: str = Query(None,  description="Type of item")):
     keys = [k for k,v in inventory.items.items() if v["store_name"]==store_name and v["product_type"]==product_type]
     if keys:
          return [inventory.items.get(key) for key in keys]
     raise HTTPException(status_code=404, detail=f"{store_name} does not have any stock of {product_type}")

        
@router.post("/create-stocklevel/{item_id}")
async def post_stocklevel(item_id: str, item: Item):
     item_dict = item.dict()
     if item_id in inventory.items.keys():
          raise HTTPException(status_code=404, detail="Item ID already exists")
     item_dict["datetime"] = datetime.now()
     inventory.items[item_id] = item_dict
     success = submit_stocklevel(item_dict)

     return inventory.items[item_id]

@router.put("/update-item/{item_id}")
async def update_stocklevel(item_id: str, item: Item):
     item_dict = item.dict()
     if item_id not in inventory.items.keys():
          raise HTTPException(status_code=404, detail="Item ID does not exists")
     item_dict["datetime"] = datetime.now()
     inventory.items[item_id]=item_dict
     return inventory.items[item_id]