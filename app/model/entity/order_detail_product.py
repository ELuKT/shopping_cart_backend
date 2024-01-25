from .order_detail import OrderDetail
from .product import Product


class OrderDetailProduct(OrderDetail):
    order_products: Product
