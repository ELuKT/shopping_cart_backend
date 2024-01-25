from beanie import PydanticObjectId
from pydantic import BaseModel

class OrderDetail(BaseModel):
    product_id: PydanticObjectId
    amount: int
    