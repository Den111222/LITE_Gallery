from uuid import UUID

from minio import Minio

from db.s3 import AbstractFileS3Repository


class MinioFileRepository(AbstractFileS3Repository):
    def __init__(self, client: Minio):
        self._client = client

    async def save_file(self, bucket_name, version_key, buffer, nbytes,
                                    content_type) -> str:
        result = self._client.put_object(bucket_name, version_key, buffer, nbytes,
                                    content_type=content_type)
        return result.object_name