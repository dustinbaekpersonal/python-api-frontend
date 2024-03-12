"""API calls defined."""
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from loguru import logger
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.models import Product, Store, User
from app.schema import Inventory

router = APIRouter()


db_dependency = Annotated[AsyncSession, Depends(get_db)]

@router.get("/users")
async def get_user_by_email(email: str, db: db_dependency):
    """Retrieve user information by email."""
    statement = select(User).where(User.email == email)
    result = await db.execute(statement)
    result = result.scalars().first()

    if not result:
        raise HTTPException(status_code=404, detail=f"User with email '{email}' not found.")
    return result


@router.get("/inventory/{store_name}")
async def fetch_product_by_store_id(store_name: str, db: db_dependency):
    """Read product stock level by store_id."""
    # Check if the store exists
    statement = select(Store).where(Store.store_name == store_name)
    result = await db.execute(statement)
    store = result.scalars().all()

    if len(store) > 1:
        logger.debug(f"This is store object {store}.")
        raise HTTPException(
            status_code=500, detail=f"Store name {store_name} cannot be duplicated."
        )

    if not store:
        raise HTTPException(status_code=404, detail=f"Store '{store_name}' not found.")

    store = store[0]

    statement_product = (
        select(Product)
        .where(Product.store_id == store.id, Store.store_name == store_name)
    )
    result = await db.execute(statement_product)
    result = result.scalars().all()

    if not result:
        raise HTTPException(
            status_code=404, detail=f"Store {store_name} does not have any inventory."
        )
    return result


# helper function to create store and inventory for the first time
async def create_inventory(inventory: Inventory, db: db_dependency):
    """Create store and product object in Postgresql database."""
    db_store = Store(store_name=inventory.store_name)
    db.add(db_store)
    await db.commit()
    db.refresh(db_store)

    for product in inventory.product_detail:
        db_product = Product(
            product_name=product.product_name,
            stock_level=product.stock_level,
            # updated_at=product.updated_at,
            store_id=db_store.id,
        )
        db.add(db_product)
    await db.commit()


@router.put("/inventory/")
async def update_inventory(inventory: Inventory, db: db_dependency):
    """Update stock level of given product and store."""
    # Check if the store exists
    statement = select(Store).filter(Store.store_name == inventory.store_name)
    result = await db.execute(statement)
    store = result.scalars().first()

    if not store:
        logger.info(f"Store '{inventory.store_name}' not found. Create store first.")
        return await create_inventory(inventory, db)

    for product_info in inventory.product_detail:
        # Check if the product exists for the given store
        product = (
            select(Product)
            .where(
                Product.store_id == store.id,
                Product.product_name == product_info.product_name,
            )
        )
        product = await db.execute(product)
        product = product.scalars().first()

        if not product:
            logger.info(
                f"Product '{product_info.product_name}' not found "
                + f"for store '{inventory.store_name}'."
            )
            logger.info("Populating product...")
            db_product = Product(
                product_name=product_info.product_name,
                stock_level=product_info.stock_level,
                # updated_at=product_info.updated_at,
                store_id=store.id,
            )
            db.add(db_product)
            continue

        # Update stock level
        product.stock_level = product_info.stock_level
        # product.updated_at = product_info.updated_at

    await db.commit()
