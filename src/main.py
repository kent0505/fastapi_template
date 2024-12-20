from fastapi                 import FastAPI
from fastapi.staticfiles     import StaticFiles

from src.core.middlewares    import setup_middlewares
from src.core.utils          import lifespan
from src.core.settings       import settings
from src.routers.parser      import router as parser_router
from src.routers.clover.home import router as clover_home_router

app = FastAPI(
    lifespan=lifespan,
    swagger_ui_parameters=settings.swagger_ui_parameters,
)

setup_middlewares(app)

app.mount(app=StaticFiles(directory="static"),    path="/static")
app.mount(app=StaticFiles(directory="templates"), path="/templates")

app.include_router(clover_home_router, include_in_schema=False)
app.include_router(parser_router, prefix="/api/v1/parser", tags=["Parser"])

# venv\Scripts\activate or source venv/bin/activate
# pip install -r requirements.txt
# uvicorn src.main:app --reload
# alembic revision --autogenerate -m ""
# alembic upgrade head
