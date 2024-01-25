from beanie import Document

class Product(Document):
    name: str
    price: str
    description: str
    remain: int
    version: int
    is_available: bool

    class Settings:
        name = "product"
