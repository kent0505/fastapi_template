from fastapi             import FastAPI, Depends
from fastapi.staticfiles import StaticFiles
from contextlib          import asynccontextmanager
from dotenv              import load_dotenv
from core.middlewares    import setup_middlewares
from core.jwt_handler    import JWTBearer
from database.base       import Base
from database.db_helper  import db_helper
from routers.user        import router as user_router
from routers.test        import router as test_router
from routers.category    import router as category_router
from routers.product     import router as product_router
from routers.order       import router as order_router
import logging

@asynccontextmanager
async def lifespan(app: FastAPI):
    # startup
    load_dotenv()
    # logging.basicConfig(
    #     filename = "logfile.log",
    #     level    = logging.INFO,
    #     format   = "%(asctime)s - %(levelname)s - %(message)s",
    #     datefmt  = "%d-%m-%Y %H:%M:%S" # 29-01-2024 14:19:28,
    # )
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

app.include_router(user_router,     prefix="/api/v1/user",     tags=["User"])
app.include_router(category_router, prefix="/api/v1/category", tags=["Category"], dependencies=[Depends(JWTBearer())])
app.include_router(product_router,  prefix="/api/v1/product",  tags=["Product"],  dependencies=[Depends(JWTBearer())])
app.include_router(order_router,    prefix="/api/v1/order",    tags=["Order"],    dependencies=[Depends(JWTBearer())])
app.include_router(test_router,     prefix="/api/v1/test",     tags=["Test"],     dependencies=[Depends(JWTBearer())])

# pip install -r requirements.txt
# uvicorn main:app --reload
# cd Desktop/backend/fastapi && venv\Scripts\activate
# eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6MSwiZXhwaXJ5IjoxNzMzNDAzMjg2fQ.SsaVF1-ywCI--lzECX4fHanCtZH21sEwwtVQuCgtPvw