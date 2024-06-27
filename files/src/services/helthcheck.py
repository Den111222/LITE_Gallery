import asyncio
import time

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from db.cache.cache_factory import get_file_cache
from db.s3.s3_factory import get_file_s3
from db.storage import get_session
from models.schemas.healthcheck import HealthCheck


class HealthCheckService:
    def __init__(self, session: AsyncSession):
        self._session = session

    @staticmethod
    async def get_status() -> HealthCheck:
        response = {
            "status": "OK",
            "message": "Service is available right now.",
        }
        return HealthCheck(**response)

    async def measure_response_time(self, action, name):
        start_time = time.time()
        try:
            self.actions(action)
            response_time = time.time() - start_time
        except Exception:
            response_time = -1
        return name, round(response_time, 6)

    async def ping(self):
        actions_to_measure = {
            "db": self.measure_response_time(self._session.execute("SELECT 1"), "db"),
            "minio": self.measure_response_time(get_file_s3(), "s3"),
            "redis": self.measure_response_time(get_file_cache(), "cache"),
        }
        results = await asyncio.gather(*actions_to_measure.values())
        response_times = {name: time for name, time in results}
        return response_times

    def actions(self, action):
        action
        time.sleep(10**-9)

def get_file_service(_session: AsyncSession = Depends(get_session)) -> HealthCheckService:
    return HealthCheckService(_session)