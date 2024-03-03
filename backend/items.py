"""API calls defined."""
from typing import Annotated

from database import Base, SessionLocal, engine
from fastapi import APIRouter, Depends, HTTPException
from models import Product, Store
from schema import Inventory
from sqlalchemy.orm import Session

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
    store = db.query(Store).filter(Store.store_name == store_name).first()
    if not store:
        raise HTTPException(status_code=404, detail=f"Store '{store_name}' not found.")

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


@router.post("/inventory/")
async def create_inventory(inventory: Inventory, db: db_dependency):
    """Create store and product object in Postgresql database."""
    db_store = Store(store_name=inventory.store_name)
    db.add(db_store)
    db.commit()
    db.refresh(db_store)

    for product in inventory.product_name:
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
        raise HTTPException(
            status_code=404, detail=f"Store '{inventory.store_name}' not found."
        )

    for product_info in inventory.product_name:
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
            raise HTTPException(
                status_code=404,
                detail=f"Product '{product_info.product_name}' not found "
                + f"for store '{inventory.store_name}'.",
            )

        # Update stock level
        product.stock_level = product_info.stock_level
        product.updated_date = product_info.updated_date

    db.commit()
