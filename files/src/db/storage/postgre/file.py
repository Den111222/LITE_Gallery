from uuid import uuid4, UUID

from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from db.storage import AbstractFileRepository
from models.schemas.file import File, FileCreateDB, FileListByProject
from models.db.file import File as DBTableFile


class FileRepository(AbstractFileRepository):

    def __init__(self, db: AsyncSession):
        self._db = db

    async def get_file_by_id(self, id: UUID) -> File | None:
        stmt = select(DBTableFile).filter(DBTableFile.id == id)

        result = await self._db.execute(stmt)
        result = result.scalar_one_or_none()

        if result is not None:
            return File.model_validate(result)

    async def get_files_by_project_id(self, project_id: str) -> FileListByProject | None:
        stmt = select(DBTableFile).filter(DBTableFile.project_id == project_id)

        result = await self._db.execute(stmt)
        result = result.all()

        if result is not None:
            files = [File.model_validate(*file) for file in result]
            return FileListByProject(project_id=project_id, files=files)

    async def create_file(self, _file: FileCreateDB) -> File:
        db_file = DBTableFile(id=uuid4(), **_file.model_dump())

        self._db.add(db_file)
        try:
            await self._db.commit()
        except IntegrityError:
            await self._db.rollback()
            return None

        await self._db.refresh(db_file)

        return File.model_validate(db_file)
