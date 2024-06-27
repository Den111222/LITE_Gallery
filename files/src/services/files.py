import json
import uuid
from io import BytesIO

from PIL.Image import Resampling

from minio import S3Error
import backoff

from core.config import app_settings
from db.storage.repo_factory import get_file_repo
from db.cache.cache_factory import get_file_cache
from db.s3.s3_factory import get_file_s3
from db.storage import AbstractFileRepository
from db.cache import AbstractCacheFileRepository
from db.s3 import AbstractFileS3Repository
from fastapi import Depends, HTTPException

from PIL import Image
from models.schemas.file import File, FileUpload, FileCreateCache, FileCreateDB, State
from models.schemas.models_base import BaseResponseBody
from services.connections import ConnectionManager, manager


versions = app_settings.versions


class FileService:
    def __init__(self, repo: AbstractFileRepository,
                 cache: AbstractCacheFileRepository,
                 s3: AbstractFileS3Repository,
                 ):
        self._repo = repo
        self._cache = cache
        self._s3 = s3
        self._manager = manager


    async def get_project_images(self, project_id: str) -> BaseResponseBody:
        files = await self._repo.get_files_by_project_id(str(project_id))

        if files is None:
            raise HTTPException(status_code=404, detail="Project not found")
        return BaseResponseBody(data={"images": files})

    @backoff.on_exception(backoff.expo, Exception, max_time=2, max_tries=10)
    async def upload_image(self, image_id: uuid, file) -> BaseResponseBody:
        file_in_cache = await self._cache.get_file_by_id(image_id)

        if file_in_cache is None:
            raise HTTPException(status_code=404, detail="Link not found, recreate link")

        file_in_cache.decode('utf-8')
        cache_dict = json.loads(file_in_cache)
        project_id = cache_dict['project_id']
        contents = await file.read()
        image = Image.open(BytesIO(contents))
        image_key = f"{project_id}/original/{image_id}"
        buffer = BytesIO()
        image.save(buffer, format=file.content_type.split("/")[1].upper())
        buffer.seek(0)
        path = await self.save_file_in_s3(file_location=image_key, contents=buffer, file=file)
        file_in_cache = FileCreateCache(**cache_dict)
        if file_in_cache.state != State.DONE:
            file_in_cache.versions["original"]["file_path"] = path.path
            file_in_cache.state = State.PROCESSING
            await self._cache.save_file(image_id, file_in_cache.json(), living_time=app_settings.living_time)
            for version, size in versions.items():
                if version == "original":
                    continue
                resized_image = await self.resize_image(image, size['size'])
                buffer = BytesIO()
                resized_image.save(buffer, format=file.content_type.split("/")[1].upper())
                buffer.seek(0)
                version_key = f"{project_id}/{version}/{image_id}"
                path = await self.save_file_in_s3(file_location=version_key, contents=buffer, file=file)
                file_in_cache.versions[version]["file_path"] = path.path
                file_in_cache.versions[version]["size"] = size['size']
                await self._cache.save_file(image_id, file_in_cache.json(), living_time=app_settings.living_time)
            file_in_cache.state = State.UPLOADED
            await self._cache.save_file(image_id, file_in_cache.json(), living_time=app_settings.living_time)
            try:
                file_in_db = await self.save_file_in_db(FileCreateDB(name=file_in_cache.name,
                                                                     project_id=file_in_cache.project_id,
                                                                     versions=file_in_cache.versions
                                                                     ))
            except Exception as e:
                file_in_cache.state = State.ERROR
                raise HTTPException(status_code=400, detail=str(e))
        await self._manager.send_message(file_in_db.project_id, f"Image {image_id} processing done")
        return BaseResponseBody(data={"message": "Image uploaded successfully"})

    async def resize_image(self, image: Image, size: tuple):
        # Calculate aspect ratio to maintain proportions
        width, height = image.size
        aspect_ratio = width / height

        # Calculate new dimensions based on target length
        if width > height:
            new_width = size[0]
            new_height = int(size[0] / aspect_ratio)
        else:
            new_height = size[1]
            new_width = int(size[1] * aspect_ratio)

        # Resize image
        resized_img = image.resize((new_width, new_height), Resampling.NEAREST)
        return resized_img

    async def save_file_in_s3(self, file_location, contents, file):
        try:
            result = await self._s3.save_file(app_settings.bucket_name, file_location,
                                               contents, contents.getbuffer().nbytes,
                                               content_type=file.content_type)
            return FileUpload(path=result)
        except S3Error as e:
            raise HTTPException(status_code=500, detail="File upload to MinIO failed")

    async def save_file_in_db(self, _file: FileCreateDB) -> File:
        file = await self._repo.create_file(_file)
        return file

    async def get_upload_link(self, filename: str, project_id: int) -> BaseResponseBody:
        image_id = str(uuid.uuid4())
        _file = FileCreateCache(project_id=str(project_id),
                           name=filename)

        file_in_cache = await self._cache.save_file(image_id, _file.json(), living_time=app_settings.living_time)
        if file_in_cache is None:
            raise HTTPException(status_code=404, detail="File not created")
        upload_link = f"/upload_file/{image_id}"
        return BaseResponseBody(data={"upload_link": upload_link, "params": {"project_id": project_id},
                                      "message": f"Link valid for {app_settings.living_time} minutes"})


def get_file_service(repo: AbstractFileRepository = Depends(get_file_repo),
                     cache: AbstractCacheFileRepository = Depends(get_file_cache),
                     s3: AbstractFileS3Repository = Depends(get_file_s3)
                     ) -> FileService:
    return FileService(repo, cache, s3)
