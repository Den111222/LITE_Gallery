from datetime import timedelta
from functools import cached_property
from logging import config as logging_config

from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field

from core.logger import LOGGING

logging_config.dictConfig(LOGGING)


class AppSettings(BaseSettings):
    project_name: str = 'File Saving Service'

    model_config = SettingsConfigDict(
        case_sensitive=False,
        env_file="../../.env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    static_files_directory: str = Field(default="templates", validation_alias="STATIC_FILES_DIRECTORY")

    versions: dict = {
        "original": {"size": "", "file_path": ""},
        "thumb": {"size": (150, 120), "file_path": ""},
        "big_thumb": {"size": (700, 700), "file_path": ""},
        "big_1920": {"size": (1920, 1080), "file_path": ""},
        "d2500": {"size": (2500, 2500), "file_path": ""},
    }

    cdn_host: str = Field(default="127.0.0.1", validation_alias="CDN_HOST")
    cdn_port: int = Field(default=8080, validation_alias="CDN_PORT")

    postgres_db: str = Field(default="files", validation_alias="POSTGRES_DB")
    postgres_user: str = Field(default="app", validation_alias="POSTGRES_USER")
    postgres_password: str = Field(default='qwe123', validation_alias="POSTGRES_PASSWORD")
    postgres_host: str = Field(default="127.0.0.1", validation_alias="POSTGRES_HOST")
    postgres_port: int = Field(default=25432, validation_alias="POSTGRES_PORT")
    echo_engine: bool = Field(default=True, validation_alias="echo_engine")

    redis_host: str = Field(default="127.0.0.1", validation_alias="REDIS_HOST")
    redis_port: int = Field(default=26379, validation_alias="REDIS_PORT")
    living_time: timedelta = Field(default=timedelta(minutes=30), validation_alias="LIVING_TIME")

    endpoint: str = Field(default="127.0.0.1:9000", validation_alias="MINIO_STORAGE_ENDPOINT")
    external_endpoint: str = Field(default="127.0.0.1:9001", validation_alias="MINIO_STORAGE_ENDPOINT")
    access_key: str = Field(default="minioadmin", validation_alias="MINIO_ACCESS_KEY")
    secret_key: str = Field(default="minioadmin", validation_alias="MINIO_SECRET_KEY")
    bucket_name: str = Field(default="files", validation_alias="MINIO_BUCKET")

    @cached_property
    def database_dsn(self) -> str:
        return (
            f"postgresql+asyncpg://{self.postgres_user}:"
            f"{self.postgres_password}@{self.postgres_host}:"
            f"{self.postgres_port}/{self.postgres_db}"
        )

    @cached_property
    def base_url(self) -> str:
        return f"http://{self.cdn_host}:{self.cdn_port}"

app_settings = AppSettings()