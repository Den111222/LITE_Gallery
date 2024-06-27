from datetime import timedelta

from redis.asyncio import Redis

from db.cache import AbstractCacheFileRepository


class RedisFileRepository(AbstractCacheFileRepository):

    def __init__(self, redis: Redis):
        self._cache = redis

    async def is_exists(self, file: str) -> bool:
        result = await self._cache.get(file)
        return bool(result)

    async def save_file(self, image_id: str, file: str, living_time: timedelta) -> None:
        result = await self._cache.set(image_id, file, living_time)
        return result

    async def get_file_by_id(self, image_id: str) -> dict:
        result = await self._cache.get(image_id)
        return result