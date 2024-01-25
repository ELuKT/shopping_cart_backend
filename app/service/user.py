from app.config import *
from app.model.entity import User

async def get_user(*args) -> User:
    user = await User.find_one(*args)
    return user

async def insert_user(**kwargs) -> User:
    user = await User(**kwargs).insert()
    return user

async def update_user(user: User, native_condition: dict):
    await user.update({"$set": native_condition})
