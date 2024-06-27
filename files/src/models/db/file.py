from sqlalchemy import Column, String, Uuid, DateTime, JSON
from datetime import datetime

from models.db import Base


class File(Base):
    __tablename__ = 'files'
    id = Column(Uuid, primary_key=True)
    name = Column(String, nullable=False, unique=True)
    project_id = Column(String, nullable=False)
    created_ad = Column(DateTime, default=datetime.utcnow)
    versions = Column(JSON)
