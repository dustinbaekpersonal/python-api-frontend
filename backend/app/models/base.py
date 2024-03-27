"""Base models for other models to inherit from."""
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    """Base declarative."""

    async def create(self, db: AsyncSession):
        """Create the user in the database."""
        db.add(self)
        await db.commit()
        await db.refresh(self)
        return True

    async def delete(self, db: AsyncSession):
        """Delete the user from database."""
        # self is instance of table object/class
        await db.delete(self)
        await db.commit()
        return True
