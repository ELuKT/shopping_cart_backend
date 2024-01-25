from typing import List
from fastapi import APIRouter, Depends
from app.config.jwt_bearer import get_current_user
from app.model.entity import Order, User, ShoppingRecord
from app.model.res.order_detail_res import OrderDetailRes
from app.model.res.shopping_record_res import ShoppingRecordRes


router = APIRouter()


@router.get('/shopping_records', response_model=List[Order])
async def get_shopping_records(user: User = Depends(get_current_user)):
    return user.records


@router.get('/shopping_record/{order_id}', response_model=ShoppingRecordRes)
async def get_shopping_record_by_id(order_id: str, user: User = Depends(get_current_user)):
    shopping_record: List[ShoppingRecord] = await user.aggregate([
        {
            '$project': {
                'records': {
                    '$filter': {
                        'input': '$records',
                        'as': 'record',
                        'cond': {'$eq': ['$$record.order_id', order_id]}
                    }
                }
            }
        },
        {'$unwind': {'path': '$records'}},
        {'$unwind': {'path': '$records.order_details'}},
        {
            '$lookup': {
                'from': 'product',
                'localField': 'records.order_details.product_id',
                'foreignField': '_id',
                'as': 'records.order_details.order_products'
            }
        },
        {'$unwind': {'path': '$records.order_details.order_products'}},
        {
            '$group': {
                '_id': '$records.order_id',
                'order_details': {
                    '$push': '$records.order_details'
                },
                'total_amount': {'$first': '$records.total_amount'},
                'create_date': {'$first': '$records.create_date'}
            }
        }
    ],
        projection_model=ShoppingRecord
    ).to_list()

    order_details: List[OrderDetailRes] = [
        OrderDetailRes(
            product_id=str(order_detail.product_id),
            name=order_detail.order_products.name,
            price=order_detail.order_products.price,
            description=order_detail.order_products.description,
            amount=order_detail.amount
        ) for order_detail in shopping_record[0].order_details
    ]

    return ShoppingRecordRes(
        id=shopping_record[0].id,
        order_details=order_details,
        total_amount=shopping_record[0].total_amount,
        create_date=shopping_record[0].create_date,
    )
