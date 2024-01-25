from datetime import datetime
from typing import List
from pydantic import BaseModel
from .order_detail import OrderDetail


class Order(BaseModel):
    order_id: str
    total_amount: str
    create_date: float = datetime.now().timestamp()
    order_details: List[OrderDetail]
