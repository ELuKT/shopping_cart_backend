from typing import List
from pydantic import BaseModel, Field
from app.model.entity.order_detail_product import OrderDetailProduct


class ShoppingRecord(BaseModel):
    id: str = Field(None, alias="_id")
    order_details: List[OrderDetailProduct]
    total_amount: str
    create_date: float