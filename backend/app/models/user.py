"""Declarative ORM models for user."""
from sqlalchemy import Integer, String, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import Base


class User(Base):  # type: ignore
    """User orm model class.

    Attributes:
        id (int): unique ID assigned for each user
        first_name (str): first name of the user
        last_name (str): last name of the user
        email (str): email of the user

    Methods:
        __repr__: to print out User class with attributes
    """

    __tablename__ = "users"
    __table_args__ = UniqueConstraint(
        "first_name", "last_name", "email", name="unique_hash_user"
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    first_name: Mapped[str] = mapped_column(String, nullable=False)
    last_name: Mapped[str] = mapped_column(String, nullable=False)
    email: Mapped[str] = mapped_column(String, nullable=False)

    def __repr__(self) -> str:
        """Return string representation of class."""
        return (
            f"User detail: ID={self.id}, First Name={self.first_name} \n"
            + f"Last Name={self.last_name}, Email={self.email}"
        )
