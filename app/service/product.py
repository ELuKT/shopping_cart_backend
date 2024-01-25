
from typing import Dict, List, Union
from app.model.common.enums import ErrorCode
from app.model.common.sc_exception import SCException
from app.model.entity import *
from app.config.redis_cache import RedisCache
from app.model.common import RedisKeys
from app.model.entity.order_detail import OrderDetail
from fastapi import status
from pymongo.errors import PyMongoError


async def is_product_available(product_id: str) -> bool:
    value:Union[str, None] = await RedisCache.hget(RedisKeys.PRODUCT_CACHE.value, product_id)
    if not value:
        product: Union[Product, None] = await Product.get(product_id)
        if product and product.is_available:
            await RedisCache.hsetnx(RedisKeys.PRODUCT_CACHE.value, str(product.id), str(product.is_available))
            return True

    return value == 'True'


async def all_product() -> List[Product]:
    products = await Product.find_all().to_list()
    return products

async def get_existing_products() -> List[Product]:
    products = await Product.find(Product.remain!=0).to_list()
    return products
