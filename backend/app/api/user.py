"""API calls for user are defined."""
from typing import Annotated

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.models.user import User

router = APIRouter(prefix="/user")


db_dependency = Annotated[AsyncSession, Depends(get_db)]


@router.get("/{email}")
async def get_user_by_email(email: str, db: db_dependency):
    """Retrieve user information by email."""
    return await User.search(email, db)
