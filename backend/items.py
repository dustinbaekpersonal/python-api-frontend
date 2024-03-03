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


@router.get("/get_inventory/{store_id}")
async def fetch_product_by_store_id(store_id: str, db: db_dependency):
    """Read product stock level by store_id."""
    result = db.query(Product).filter(Product.store_id == store_id).all()
    if not result:
        raise HTTPException(status_code=404, detail="Store is not found.")
    return result


@router.post("/create_inventory/")
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
            created_date=product.created_date,
            store_id=db_store.id,
        )
        db.add(db_product)
    db.commit()
