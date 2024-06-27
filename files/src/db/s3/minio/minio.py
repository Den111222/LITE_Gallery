from minio import Minio

from core.config import app_settings


MINIO_URL = app_settings.external_endpoint
MINIO_ACCESS_KEY = app_settings.access_key
MINIO_SECRET_KEY = app_settings.secret_key
MINIO_BUCKET_NAME = app_settings.bucket_name


async def get_minio() -> Minio:
    minio_client = Minio(
        MINIO_URL,
        access_key=MINIO_ACCESS_KEY,
        secret_key=MINIO_SECRET_KEY,
        secure=False
    )

    # Ensure the bucket exists
    found = minio_client.bucket_exists(MINIO_BUCKET_NAME)
    if not found:
        minio_client.make_bucket(MINIO_BUCKET_NAME)
    yield minio_client