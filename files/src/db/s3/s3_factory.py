from functools import lru_cache
from fastapi import Depends
from minio import Minio

from db.s3.minio.files import MinioFileRepository
from db.s3.minio.minio import get_minio


@lru_cache()
def get_file_s3(
    client: Minio = Depends(get_minio),
) -> MinioFileRepository:
    return MinioFileRepository(client)