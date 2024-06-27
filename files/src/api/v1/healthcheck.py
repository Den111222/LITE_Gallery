from fastapi import APIRouter, Depends

from models.schemas.healthcheck import HealthCheck
from services.helthcheck import (
    HealthCheckService as service, get_file_service, HealthCheckService
)


router = APIRouter(prefix="/healthcheck")


@router.get("/", response_model=HealthCheck, summary="Get application state")
async def get_service_status() -> HealthCheck:
    return await service.get_status()


@router.get("/ping")
async def ping(service: HealthCheckService = Depends(get_file_service)):
    result = await service.ping()
    return result
