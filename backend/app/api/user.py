"""API calls for user are defined."""
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from loguru import logger
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.models.user import User

router = APIRouter(prefix="/user")


db_dependency = Annotated[AsyncSession, Depends(get_db)]


@router.get("/{email}")
async def get_user_by_email(email: str, db: db_dependency):
    """Retrieve user information by email."""
    statement = select(User).where(User.email == email)
    result = await db.execute(statement)
    result = result.scalars().first()
    logger.debug(result)

    if not result:
        raise HTTPException(status_code=404, detail=f"User with email '{email}' not found.")
    return result