from typing import List
from fastapi import APIRouter
from app.model.entity import Product
from app.model.res.product_res import ProductRes
from app.service.product import get_existing_products

router = APIRouter()


@router.get('/', response_model=List[ProductRes], response_model_by_alias=False) # response_model_by_alias prevent response use _id as variable name
async def get_products():
    products = await get_existing_products()
    return products


@router.get('/{id}', response_model=ProductRes, response_model_by_alias=False)
async def get_product_by_id(id):
    return await Product.get(id)
