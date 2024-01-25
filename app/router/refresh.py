from fastapi import APIRouter
from beanie import BulkWriter
from app.config.redis_cache import RedisCache
from app.model.common.enums import RedisKeys

from app.model.entity import *

router = APIRouter()

@router.post('/')
async def refresh():
    products:List[Product] = await Product.find_all().to_list()
    deprecated = []
    for product in products:
        deprecated.append(str(product.id))
        deprecated.append('False')
    await RedisCache.hset(RedisKeys.PRODUCT_CACHE.value, deprecated)
    await Product.delete_all()
    await Product.insert_many(
        [
            Product(name="Product1", price = "0.1", description="this is product1", remain=5, version=0, is_available=True),
            Product(name="Product2", price = "0.2", description="this is product2", remain=5, version=0, is_available=True),
            Product(name="Product3", price = "0.3", description="this is product3", remain=5, version=0, is_available=True),
        ]
    )

    await CustomException.delete_all()
    await CustomException.insert_many(
        [
            CustomException(error_code="SC001", description = 'Could not validate JWT'),
            CustomException(error_code="SC002", description = 'Could not find user email in JWT'),
            CustomException(error_code="SC003", description = 'Email or password is wrong'),
            CustomException(error_code="SC004", description = 'User not found'),
            CustomException(error_code="SC005", description = 'System busy, please try again later'),
            CustomException(error_code="SC006", description = 'You tried signing in with a different authentication method than the one you used during signup. Please try again using your original authentication method.'),
            CustomException(error_code="SC007", description = 'Your authentication method does not support email validation.'),
            CustomException(error_code="SC008", description = 'User already exists'),
            CustomException(error_code="SC009", description = 'We ran into an issue while signing you in, please take a break and try again soon.'),
            CustomException(error_code="SC010", description = '{product_name} sold out'),
            CustomException(error_code="SC011", description = '{product_name} only {remain} left'),
            CustomException(error_code="SC012", description = 'Product not found'),
            CustomException(error_code="SC013", description = 'Cart is empty'),
            CustomException(error_code="SC014", description = 'Remove amount greater than the amount in the cart'),
        ]
    )
