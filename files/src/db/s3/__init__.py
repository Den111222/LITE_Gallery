from abc import ABC, abstractmethod
from uuid import UUID


class AbstractFileS3Repository(ABC):

    @abstractmethod
    async def save_file(self, s3_schema: dict) -> str:
        raise NotImplementedError