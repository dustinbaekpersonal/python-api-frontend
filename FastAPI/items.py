import os

import pandas as pd
import yaml
from schema import Item, Product

from fastapi import APIRouter, HTTPException, Query

DB_FILEPATH = "db/stock_levels.parquet"

with open("../config.yml", "r") as stream:
    config = yaml.safe_load(stream)

router = APIRouter()


@router.get("/stock-levels")
async def get_stock_levels(product: Product = Query(None, description="Product type")) -> dict:
    """Get the stock level of a product in a store

    Parameters
    ----------
    product : Product, optional
        product name, by default Query(None, description="Type of item")

    Returns
    -------
    Dict
        dictionary of stock levels for each store for the product

    Raises
    ------
    HTTPException
        When the product is not found
    """
    if product.name not in config["products"]:
        raise HTTPException(status_code=404, detail="Item not found")
    db = _read_db()
    return db.loc[product.name].fillna("").to_dict()


@router.put("/stock-levels")
async def put_stock_levels(item: Item) -> dict:
    """Update the stock level of a product in a store
    
    Parameters
    ----------
    item : Item
        Item object containing the product, store, stock level and datetime
    
    Returns
    -------
    Dict
        message confirming the stock level was submitted
    """
    db = _read_db()
    db.loc[(item.product.value, item.store.value)] = [item.stock_level, item.datetime]
    db.to_parquet(DB_FILEPATH, engine="pyarrow", compression="snappy")
    return {"message": "Stock level submitted"}


def _read_db():
    """Read the database from disk or create a new one if it doesn't exist"""
    if os.path.exists(DB_FILEPATH):
        return pd.read_parquet(DB_FILEPATH)
    os.makedirs(os.path.dirname(DB_FILEPATH), exist_ok=True)
    db_index = pd.MultiIndex.from_product([config["products"], config["stores"]], names=["product", "store"])
    return pd.DataFrame(index=db_index, columns=["stock_level", "datetime"])
