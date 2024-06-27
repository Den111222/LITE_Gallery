from functools import lru_cache

from fastapi import Depends
from redis import Redis

from db.cache import get_redis
from db.cache.redis.files import RedisFileRepository


@lru_cache()
def get_file_cache(
    session: Redis = Depends(get_redis),
) -> RedisFileRepository:
    return RedisFileRepository(session)