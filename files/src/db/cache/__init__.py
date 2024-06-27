from abc import ABC, abstractmethod
from datetime import timedelta
from uuid import UUID

from db.cache.redis.redis import get_redis


class AbstractCacheFileRepository(ABC):
    @abstractmethod
    async def is_exists(self, file: str) -> bool:
        raise NotImplementedError

    @abstractmethod
    async def save_file(self, file: str, living_time: timedelta) -> None:
        raise NotImplementedError

    @abstractmethod
    async def get_file_by_id(self, image_id: UUID) -> dict:
        raise NotImplementedError
