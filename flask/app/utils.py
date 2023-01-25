"""
Underlying API functions
"""
import os
import logging
import sys

import pandas as pd

from typing import Dict

from config import DbConfig


def create_logger(log_level: int = logging.DEBUG) -> logging.Logger:
    """ Create a logger object to be used throughout the script

    Args:
        log_level (int): The level of the logs (see https://docs.python.org/3/library/logging.html)

    Returns:
        logging.Logger: Our logging object
    """
    # Instantiate a logging object
    logger = logging.getLogger(__name__)
    # Set the level of the logs
    logger.setLevel(log_level)

    # create a logging format
    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s", "%Y-%m-%d %H:%M:%S"
    )

    # create a file and stream handler handler
    stream_handler = logging.StreamHandler(sys.stdout)
    # Set the formatting
    stream_handler.setFormatter(formatter)
    # Add the handler to the logger object
    logger.addHandler(stream_handler)

    return logger


logger = create_logger()


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

    logger.info("Writing to database file")

    # Write to the file
    db.to_csv(DbConfig["DB_FILEPATH"], index=False)

    logger.info("Wrote successfully")

    return True


def get_stocklevel(product_type: str) -> pd.DataFrame:
    """
    Get the stock level report for a given product

    Args:
        product_type (str): one of the given product types

    Returns:
        stock level report (pd.DataFrame): report of the most recent stock levels for a given product type. E.g loo roll for every location
    """
    #############################################
    # EXERCISE 4:
    #############################################
    #### WRITE YOUR CODE HERE ####



    # TEMP CHANGE WHAT IS RETURNED (hint should be a data frame in the below format)
    return pd.DataFrame(
            columns=["datetime", "resolved_address", "lat", "lng", "stock_level"]
        )
