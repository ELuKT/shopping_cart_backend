from typing import List
from pydantic import BaseModel


class OrderDetailRes(BaseModel):
    product_id: str
    name: str
    price: str
    description: str
    amount: int