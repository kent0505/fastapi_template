from fastapi             import FastAPI, Depends
from fastapi.staticfiles import StaticFiles
from contextlib          import asynccontextmanager
from database.base       import Base
from database.db_helper  import db_helper
from core.jwt_handler    import JWTBearer
from core.middlewares    import setup_middlewares
from routers.user        import router as user_router
from routers.test        import router as test_router
import logging

@asynccontextmanager
async def lifespan(app: FastAPI):
    # startup
    logging.basicConfig(
        filename = "logfile.log",
        level    = logging.INFO,
        format   = "%(asctime)s - %(levelname)s - %(message)s",
        datefmt  = "%d-%m-%Y %H:%M:%S" # 29-01-2024 14:19:28,
    )
    logging.info("STARTUP")
    async with db_helper.engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    # shutdown
    logging.info("SHUTDOWN")
    await db_helper.dispose()

app = FastAPI(
    lifespan=lifespan,
    swagger_ui_parameters={"defaultModelsExpandDepth": -1},
)

setup_middlewares(app)

app.mount(app=StaticFiles(directory="static"),    path="/static")
app.mount(app=StaticFiles(directory="templates"), path="/templates")

app.include_router(user_router, prefix="/api/v1/user", tags=["User"])
app.include_router(test_router, prefix="/api/v1/test", tags=["Test"], dependencies=[Depends(JWTBearer())])

# pip install -r requirements.txt
# uvicorn main:app --reload
# cd Desktop/backend/fastapi && venv\Scripts\activate