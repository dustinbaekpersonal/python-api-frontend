"""Schemas of User details required as an input of API request."""
from pydantic import BaseModel


class UserDetails(BaseModel):
    """Pydantic model for users."""

    first_name: str
    last_name: str
