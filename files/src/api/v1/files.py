from fastapi import APIRouter, Depends, UploadFile, File

from models.schemas.models_base import BaseResponseBody
from services.files import FileService, get_file_service

router = APIRouter(prefix="/files")


@router.get("/projects/{project_id}/images", response_model=BaseResponseBody)
async def get_project_images(project_id: int,
                     service: FileService = Depends(get_file_service)):
    result = await service.get_project_images(project_id)
    return result

@router.post("/upload/", response_model=BaseResponseBody)
async def get_upload_link(filename: str, project_id: int,
                          service: FileService = Depends(get_file_service)):
    result = await service.get_upload_link(filename, project_id)
    return result

@router.post("/upload_file/{image_id}", response_model=BaseResponseBody)
async def upload_image(image_id: str, file: UploadFile = File(...),
                       service: FileService = Depends(get_file_service)):
    result = await service.upload_image(image_id, file)
    return result
