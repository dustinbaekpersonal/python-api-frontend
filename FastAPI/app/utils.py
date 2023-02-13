import os
import sys

import pandas as pd
from datetime import datetime, timedelta
from typing import Dict

from config import DbConfig

def submit_stocklevel(stock_data: Dict) -> bool:
    """
    Submit a stock level of a given location to be recorded in the 'db'

    Args:
        stock_data (Dict): follows the schema of the StockLevelReportSchema object found in schema.py

    Returns:
        bool: True if successful update
    """

    # submit stock level and geocode to our "database" (CSV)
    # this is a hack for demostrative purposes only, use a SQL/ no-SQL when creating your own app and proper error handling
    # look at sql alchemy if you want to use a sql db

    if os.path.exists(DbConfig["DB_FILEPATH"]):
        db = pd.read_csv(DbConfig["DB_FILEPATH"])
    else:
        db = pd.DataFrame()
    
    timestamp = stock_data.pop("datetime").strftime(
        "%Y-%m-%dT%H:%M:%Sz"
    )  # convert timestamp to str
    stock_data["datetime"] = timestamp
    db = db.append(stock_data, ignore_index=True)

    # Write to the file
    db.to_csv(DbConfig["DB_FILEPATH"], index=False)

    return True

def add_datetime(inventory):
     for item_id in inventory.items:
          item_dict = inventory.items[item_id].dict()
          item_dict["datetime"] = datetime.now() - timedelta(1)
          inventory.items[item_id] = item_dict