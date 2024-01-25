from enum import Enum
import json
from typing import Any, Optional, Type, TypeVar, Union
from pydantic import BaseModel
from redis import RedisError
from redis.asyncio.client import Redis
from app.model.common.enums import ErrorCode, RedisKeys
from app.model.common.sc_exception import SCException
from fastapi import Depends, status
from functools import wraps
from app.service.log_service import LogService


class RedisCache:
    T = TypeVar('T')

    def simple_redis_decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            if args[1]!=RedisKeys.EMAIL_TOKEN: 
                LogService.info(f"func: {func.__name__}, args: {args[1:]}, kwargs: {kwargs}")
            try:
                res = func(*args, **kwargs)
            except:
                raise SCException(status.HTTP_503_SERVICE_UNAVAILABLE, ErrorCode.SC005)
            return res
        return wrapper

    @classmethod
    async def set_redis_cli(cls, redis_cli: Redis):
        cls.redis_cli = redis_cli

    @classmethod
    @simple_redis_decorator
    async def get_cache(cls, key: Union[str, Enum], obj_type: Type[T] = str) -> Union[T, None]:
        try:
            if isinstance(key, Enum):
                key = key.value
            
            cache_data = await cls.redis_cli.get(key)
            if cache_data:
                if issubclass(obj_type, BaseModel):
                    return obj_type(**json.loads(cache_data))
        except RedisError as e:
            raise SCException(status.HTTP_503_SERVICE_UNAVAILABLE, ErrorCode.SC005)
        return cache_data

    @classmethod
    @simple_redis_decorator
    async def set_cache(cls, key: Union[str, Enum], value: Union[str, BaseModel], ex: Optional[int] = None):
        try:
            if isinstance(key, Enum):
                key = key.value
            if isinstance(value, BaseModel):
                value = value.json()
            
            await cls.redis_cli.set(key, value, ex)
        except RedisError as e:
            raise SCException(status.HTTP_503_SERVICE_UNAVAILABLE, ErrorCode.SC005)
        
    @classmethod
    @simple_redis_decorator
    async def hincrby(cls, key: str, field: str, amount: int):
        await cls.redis_cli.hincrby(key, field ,amount)
        

    @classmethod
    @simple_redis_decorator
    async def hgetall(cls, key: str):
        return await cls.redis_cli.hgetall(key)
    
    # As of Redis version 4.0.0, this command is regarded as deprecated.
    @classmethod
    @simple_redis_decorator
    async def hmset(cls, key: str,  mapping: dict):
        await cls.redis_cli.hmset(key, mapping)
    
    @classmethod
    @simple_redis_decorator
    async def expire(cls, key: str):
        await cls.redis_cli.expire(key, 3600)

    @classmethod
    @simple_redis_decorator
    async def delete(cls, key: str):
        await cls.redis_cli.delete(key)

    @classmethod
    @simple_redis_decorator
    async def hget(cls, key: str, field: str):
        return await cls.redis_cli.hget(key, field)

    @classmethod
    @simple_redis_decorator
    async def hsetnx(cls, key: str, field: str, value):
        await cls.redis_cli.hsetnx(key, field, value)

    
    @classmethod
    @simple_redis_decorator
    async def hset(cls, key: str,  items: list):
        # https://github.com/redis/redis-py/issues/2187
        # await cls.redis_cli.hset(key, items=items)
        while len(items):
            await cls.redis_cli.hset(key, items.pop(), items.pop())

    @classmethod
    @simple_redis_decorator
    async def hdel(cls, key: str, field: str):
        await cls.redis_cli.hdel(key, field)
    