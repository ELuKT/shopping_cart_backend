from contextlib import asynccontextmanager
from typing import Union
from beanie import init_beanie
from fastapi import FastAPI
from motor.motor_asyncio import AsyncIOMotorClient
import redis.asyncio as redis
from .transaction import Transaction
from .redis_cache import RedisCache
from httpx import AsyncClient
from .settings import get_env_config
from app.model.entity import *

httpx_client: AsyncClient = AsyncClient()

@asynccontextmanager
async def lifespan(app: FastAPI):
    env_config = get_env_config()
    motor_cli = AsyncIOMotorClient(env_config.MONGODB_URL)
    await Transaction.set_motor_cli(motor_cli)
    await init_beanie(database=motor_cli[env_config.MONGODB_DATABASE_NAME], document_models=[Product, User, CustomException])
    # env is empty string when env file has no value
    redis_pool = redis.BlockingConnectionPool(host=env_config.REDIS_HOST, port=env_config.REDIS_PORT, password=env_config.REDIS_PASSWORD, decode_responses=True, timeout=5)
    redis_cli = redis.Redis(connection_pool=redis_pool)
    await RedisCache.set_redis_cli(redis_cli)
    yield
    motor_cli.close()
    await httpx_client.aclose()
    await redis_cli.close()
    