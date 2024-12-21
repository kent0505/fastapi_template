from fastapi            import APIRouter, Request
from fastapi.templating import Jinja2Templates

import os

router = APIRouter()
templates = Jinja2Templates(directory="templates")

@router.get("/")
async def home(request: Request):
    return templates.TemplateResponse("index.html", {
        "request": request,
        "url": "os.getenv("")"
    })
