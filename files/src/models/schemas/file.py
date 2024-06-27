from datetime import datetime
from enum import Enum
from uuid import UUID
from pydantic import BaseModel, ConfigDict
from core.config import app_settings


class State(Enum):
    INIT = 'init'
    UPLOADED = 'uploaded'
    PROCESSING = 'processing'
    ERROR = 'error'
    DONE = 'done'

class FileBase(BaseModel):
    name: str
    project_id: str

class FileUpload(BaseModel):
    path: str

class FileCreateDB(FileBase):
    versions: dict

class FileCreateCache(FileBase):
    versions: dict = app_settings.versions
    state: State = State.INIT

    model_config = ConfigDict(from_attributes=True)

class File(FileBase):
    id: UUID
    created_ad: datetime

    class Config:
        from_attributes = True

class FileListByProject(BaseModel):
    project_id: str
    files: list[File]