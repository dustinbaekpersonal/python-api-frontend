"""API calls for inventory are defined."""
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from loguru import logger
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.models.items import Product, Store
from app.schemas.items import Inventory

router = APIRouter(prefix="/inventory")


db_dependency = Annotated[AsyncSession, Depends(get_db)]


@router.get("/{store_name}")
async def fetch_product_by_store_id(store_name: str, db: db_dependency):
    """Fetch product's stock level by store name.

    Args:
        store_name (str): name of the stores.
        db (AsyncSession): single logical asynchronous database transaction.
    """
    # Retrieve store details given store name
    store = await Store.search(store_name, db)
    if not store:
        raise HTTPException(status_code=404, detail=f"Store '{store_name}' not found.")
    logger.info(f"Store with store name: {store_name} has {store}")
    # Search product details using store id
    products = await Product.search_by_store(store.id, db)

    return products


# helper function to create store and inventory for the first time
async def create_inventory(inventory: Inventory, db: db_dependency):
    """Create store and product object in Postgresql database.

    Args:
        inventory (Inventory): pydantic schema of Inventory defining user input.
        db (AsyncSession): single logical asynchronous database transaction.
    """
    # create an instance of Store with store_name
    db_store = Store(store_name=inventory.store_name)
    # db.add(db_store)
    # await db.commit()
    # await db.refresh(db_store)
    await db_store.create(db)

    # for each product, create Product instance and add to products table
    for product in inventory.product_detail:
        db_product = Product(
            product_name=product.product_name,
            stock_level=product.stock_level,
            store_id=db_store.id,
        )
        db.add(db_product)
    await db.commit()


@router.put("/")
async def update_inventory(inventory: Inventory, db: db_dependency):
    """Update stock level of given product and store.

    Args:
        inventory (Inventory): pydantic schema of Inventory
        db (AsyncSession): single logical asynchronous database transaction.
    """
    # Check if the store exists
    store = await Store.search(inventory.store_name, db)

    if not store:
        logger.info(f"Store '{inventory.store_name}' not found. Create store first.")
        return await create_inventory(inventory, db)

    for product_info in inventory.product_detail:
        # Check if the product exists for the given store
        product = await Product.search_by_store_product_name(
            store.id, product_info.product_name, db
        )

        if not product:
            logger.info(
                f"Product '{product_info.product_name}' not found "
                + f"for store '{inventory.store_name}'."
            )
            logger.info("Populating product...")
            db_product = Product(
                product_name=product_info.product_name,
                stock_level=product_info.stock_level,
                store_id=store.id,
            )
            db.add(db_product)
            continue

        # Update stock level
        product.stock_level = product_info.stock_level

    await db.commit()
