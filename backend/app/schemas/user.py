"""Schemas of User details required as an input of API request."""
from pydantic import BaseModel, ConfigDict

config = ConfigDict(from_attributes=True)


class UserIn(BaseModel):
    """Pydantic model for users when logging in."""

    model_config = config
    username: str
    full_name: str | None = None
    email: str
    password: str


class UserOut(BaseModel):
    """Pydantic model for users other than logging in."""

    username: str
    full_name: str | None = None
    email: str
