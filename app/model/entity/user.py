from beanie import Document, Indexed
from pydantic import EmailStr, Field
from typing import List
from .order import Order


class User(Document):
    email: Indexed(EmailStr, unique=True)
    hashed_password: str
    is_validated: bool
    state: str
    auth_method: str
    records: List[Order]

    class Settings:
        name = "user"