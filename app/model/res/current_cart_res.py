from typing import List
from pydantic import BaseModel
from app.model.res.cart_product import CartProduct


class CurrentCartRes(BaseModel):
    cart_products: List[CartProduct]
