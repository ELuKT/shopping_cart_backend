import asyncio
from datetime import datetime
from typing import Dict, List, Union
from beanie import BulkWriter
from bson import ObjectId
from fastapi import APIRouter, Depends, status
from app.config.transaction import Transaction
from app.config.jwt_bearer import get_current_user
from app.model.entity import *
from app.model.common import *
from app.model.req.cart_req import CartReq
from app.model.res.cart_product import CartProduct
from app.model.res.current_cart_res import CurrentCartRes
from app.config.redis_cache import RedisCache
from app.service.log_service import LogService
from app.service.product import all_product, is_product_available
import time
from pymongo.errors import PyMongoError
from pymongo.results import UpdateResult

router = APIRouter()


@router.post('/add', response_model=None)
async def add_cart(cart_req: CartReq, user: User = Depends(get_current_user)):
    is_available:bool = await is_product_available(cart_req.product_id)
    if not is_available:
        raise SCException(status.HTTP_404_NOT_FOUND, ErrorCode.SC012)
    cart_key = RedisKeys.USER_CART.value.format(user_email=user.email)
    await RedisCache.hincrby(cart_key, cart_req.product_id, cart_req.amount)
    await RedisCache.expire(cart_key)

@router.delete('/remove', response_model=None)
async def remove_cart(cart_req: CartReq, user: User = Depends(get_current_user)):
    is_available:bool = await is_product_available(cart_req.product_id)
    if not is_available:
        raise SCException(status.HTTP_404_NOT_FOUND, ErrorCode.SC012)
    cart_key = RedisKeys.USER_CART.value.format(user_email=user.email)
    amount: Union[str, None] = await RedisCache.hget(cart_key, cart_req.product_id)
    if not amount or int(amount) < cart_req.amount:
        raise SCException(status.HTTP_422_UNPROCESSABLE_ENTITY, ErrorCode.SC014)
    elif int(amount) == cart_req.amount:
        await RedisCache.hdel(cart_key, cart_req.product_id)
    else:
        await RedisCache.hincrby(cart_key, cart_req.product_id, -cart_req.amount)
        await RedisCache.expire(cart_key)

@router.delete('/clear', response_model=None)
async def clear_cart(user: User = Depends(get_current_user)):
    cart_key = RedisKeys.USER_CART.value.format(user_email=user.email)
    await RedisCache.delete(cart_key)


@router.get('/show_current_cart', response_model=CurrentCartRes)
async def show_current_cart(user: User = Depends(get_current_user)):
    cart_key = RedisKeys.USER_CART.value.format(user_email=user.email)
    cart: dict = await RedisCache.hgetall(cart_key)
    products: Dict[str, Product] = {str(product.id): product for product in await all_product()}
    cart_products:List[CartProduct]=[
        CartProduct(product_id=k, 
                    product_name=products[k].name, 
                    amount=cart[k])
        for k in cart.keys()
    ]
    return CurrentCartRes(cart_products=cart_products)


@router.post('/checkout', response_model=Order)
async def checkout(user: User = Depends(get_current_user)):
    LogService.info('Checkout begin')
    cart_key = RedisKeys.USER_CART.value.format(user_email=user.email)
    cart: dict = await RedisCache.hgetall(cart_key)
    if not cart:
        raise SCException(status.HTTP_400_BAD_REQUEST, ErrorCode.SC013)
    
    # check product is available or not
    unavailable_product_ids: List[str] = [
        product_id for product_id in cart.keys() if not await is_product_available(product_id)
    ]
    if unavailable_product_ids:
        LogService.error(f'Cart has product thats not available: {unavailable_product_ids}')
        raise SCException(status.HTTP_503_SERVICE_UNAVAILABLE, ErrorCode.SC005)

    async with await Transaction.get_transaction() as s: # transaction give us non-repleatable, also rollback while exception
        async with s.start_transaction():
            total_amount=0
            products:List[Product] = await Product.find({'_id':{'$in':[ObjectId(k) for k in cart.keys()]}}).to_list()
            order_details:List[OrderDetail] = [OrderDetail(product_id = k, amount = v) for k, v in cart.items()]
            # print('sleep 5 second')
            # await asyncio.sleep(5)
            # print('slept 5 second')
            # check if 
            LogService.info('begin products calculation')
            for product in products:
                if product.remain == 0:
                    raise SCException(status.HTTP_400_BAD_REQUEST, ErrorCode.SC010, product_name=product.name)
                quantity = int(cart[str(product.id)])
                left = product.remain - quantity
                if left < 0:
                    raise SCException(status.HTTP_400_BAD_REQUEST, ErrorCode.SC011, product_name=product.name, remain=product.remain)
                
                # this is wrong operation
                # product_for_update: Product = await Product.find_one({'_id': product.id, 'version': product.version})
                # product_for_update.update({'$set':{'remain': left, 'version': product.version+1}})
                try:
                    # BEWARE: Document.update is different from FindOne.update
                    #         FindOne.update will return pymongo.results.UpdateResult, Document.update won't
                    #         find_one then update seems working like mongodb find_and_modify
                    # rollback will still work when put session just in find_one 
                    update: UpdateResult = await Product.find_one({'_id': product.id, 'version': product.version}, session=s).update({'$set':{'remain': left, 'version': product.version+1}})
                except PyMongoError as e:
                    LogService.error('product remain update exception', e)
                    raise SCException(status.HTTP_503_SERVICE_UNAVAILABLE, ErrorCode.SC005)
                if update.modified_count == 0:
                    LogService.info('product update failed')
                    raise SCException(status.HTTP_503_SERVICE_UNAVAILABLE, ErrorCode.SC005)
                total_amount = round(total_amount + quantity * float(product.price), 2)
            LogService.info('begin update user record')
            order = Order(order_id=datetime.now().strftime('%Y%m%d%H%M%S'), total_amount=total_amount, order_details=order_details)
            await user.update({'$push': {'records': order}}, session=s)
    await RedisCache.delete(cart_key)
    return order
