from fastapi            import APIRouter, Request
from fastapi.templating import Jinja2Templates

router = APIRouter()
templates = Jinja2Templates(directory="templates")

@router.get("/")
async def home(request: Request):
    return templates.TemplateResponse("index.html", {
        "request": request,
        "user_id": "",
    })

@router.get("/{user_id}")
async def home_user_id(request: Request, user_id: int):
    return templates.TemplateResponse("index.html", {
        "request": request,
        "user_id": user_id,
    })
