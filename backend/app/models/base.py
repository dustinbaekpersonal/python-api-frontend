"""Base models for other models to inherit from."""
from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    """Base declarative."""

    pass
