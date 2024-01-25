from pydantic import BaseModel, PositiveInt


class CartReq(BaseModel):
    amount: PositiveInt
    product_id: str