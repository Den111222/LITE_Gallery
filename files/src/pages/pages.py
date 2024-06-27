from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates


router = APIRouter(
    prefix="/pages",
    tags=["Pages"]
)

templates = Jinja2Templates(directory="templates")


@router.get("/")
async def read_index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@router.get("/base")
def get_base_page(request: Request):
    return templates.TemplateResponse("base.html", {"request": request})

@router.get("/ws/{project_id}")
def get_chat_page(request: Request, project_id: str):
    return templates.TemplateResponse("ws.html", {"request": request, "project_id": project_id})