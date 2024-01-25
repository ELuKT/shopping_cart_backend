from pydantic import BaseModel


class CartProduct(BaseModel):
    product_id: str
    product_name: str
    amount: int
