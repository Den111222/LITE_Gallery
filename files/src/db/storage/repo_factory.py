from functools import lru_cache

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from db.storage import get_session
from db.storage.postgre.file import FileRepository


@lru_cache()
def get_file_repo(
    session: AsyncSession = Depends(get_session),
) -> FileRepository:
    return FileRepository(session)
