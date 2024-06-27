from abc import ABC, abstractmethod
from uuid import UUID

from models.schemas.file import File
from db.storage.postgre.postgre_session import get_session


class AbstractFileRepository(ABC):

    @abstractmethod
    async def get_file_by_id(self, id: UUID) -> File | None:
        raise NotImplementedError

    @abstractmethod
    async def get_files_by_project_id(self, project_id: str) -> File | None:
        raise NotImplementedError

    @abstractmethod
    async def create_file(self, file_path: str, owner_id: int) -> File:
        raise NotImplementedError
