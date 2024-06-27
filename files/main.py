import logging
import uvicorn

from fastapi import APIRouter, FastAPI
from fastapi.responses import ORJSONResponse
from fastapi.middleware.cors import CORSMiddleware

from models.schemas.models_base import BaseExceptionBody

from api.v1 import files, healthcheck, connections
import constants as const
from core.config import app_settings, LOGGING
from pages import pages

v1_router = APIRouter(
    prefix="/api/v1",
    tags=["Files"],
)
v1_router.include_router(healthcheck.router)
v1_router.include_router(files.router)

app = FastAPI(
    title=const.APP_API_DOCS_TITLE,
    version=const.APP_VERSION,
    description=const.APP_DESCRIPTION,
    docs_url="/api/openapi",
    openapi_url="/api/openapi.json",
    default_response_class=ORJSONResponse
)

app.include_router(v1_router)
app.include_router(connections.router)
app.include_router(pages.router)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host=app_settings.cdn_host,
        port=app_settings.cdn_port,
        log_config=LOGGING,
        log_level=logging.INFO,
    )
