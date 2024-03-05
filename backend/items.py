"""API calls defined."""
import logging
from typing import Annotated

from database import Base, SessionLocal, engine
from fastapi import APIRouter, Depends, HTTPException
from models import Product, Store
from schema import Inventory
from sqlalchemy.orm import Session

logger = logging.getLogger(__name__)
logging.basicConfig(
    format="%(asctime)s : %(levelname)s : %(message)s",
    datefmt="%d/%m/%Y %H:%M:%S",
    level="DEBUG",
)

router = APIRouter()

Base.metadata.create_all(bind=engine)


def get_db():
    """Yield database instance and always close."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


db_dependency = Annotated[Session, Depends(get_db)]


@router.get("/inventory/{store_name}")
async def fetch_product_by_store_id(store_name: str, db: db_dependency):
    """Read product stock level by store_id."""
    # Check if the store exists
    store = db.query(Store).filter(Store.store_name == store_name).all()
    if len(store) > 1:
        logger.debug(f"This is store object {store}.")
        raise HTTPException(
            status_code=500, detail=f"Store name {store_name} cannot be duplicated."
        )

    if not store:
        raise HTTPException(status_code=404, detail=f"Store '{store_name}' not found.")

    store = store[0]

    result = (
        db.query(Product)
        .filter(Product.store_id == store.id, Store.store_name == store_name)
        .all()
    )

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
    db.commit()
    db.refresh(db_store)

    for product in inventory.product_detail:
        db_product = Product(
            product_name=product.product_name,
            stock_level=product.stock_level,
            updated_date=product.updated_date,
            store_id=db_store.id,
        )
        db.add(db_product)
    db.commit()


@router.put("/inventory/")
async def update_inventory(inventory: Inventory, db: db_dependency):
    """Update stock level of given product and store."""
    # Check if the store exists
    store = db.query(Store).filter(Store.store_name == inventory.store_name).first()
    if not store:
        logger.info(f"Store '{inventory.store_name}' not found. Create store first.")
        return await create_inventory(inventory, db)

    for product_info in inventory.product_detail:
        # Check if the product exists for the given store
        product = (
            db.query(Product)
            .filter(
                Product.store_id == store.id,
                Product.product_name == product_info.product_name,
            )
            .first()
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
                updated_date=product_info.updated_date,
                store_id=store.id,
            )
            db.add(db_product)
            continue

        # Update stock level
        product.stock_level = product_info.stock_level
        product.updated_date = product_info.updated_date

    db.commit()
