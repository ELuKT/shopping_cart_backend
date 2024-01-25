from typing import List
from pydantic import BaseModel
from app.model.res.order_detail_res import OrderDetailRes


class ShoppingRecordRes(BaseModel):
    id: str
    order_details: List[OrderDetailRes]
    total_amount: str
    create_date: float