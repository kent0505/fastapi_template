from fastapi              import FastAPI, Depends
from fastapi.staticfiles  import StaticFiles

from src.core.middlewares import setup_middlewares
from src.core.utils       import lifespan
from src.core.jwt_handler import JWTBearer
from src.core.settings    import settings
from src.routers.user     import router as user_router
from src.routers.test     import router as test_router
from src.routers.category import router as category_router
from src.routers.product  import router as product_router
from src.routers.order    import router as order_router

app = FastAPI(
    lifespan=lifespan,
    swagger_ui_parameters=settings.swagger_ui_parameters,
)

setup_middlewares(app)

app.mount(app=StaticFiles(directory="static"),    path="/static")
app.mount(app=StaticFiles(directory="templates"), path="/templates")

app.include_router(user_router,     prefix="/api/v1/user",     tags=["User"])
app.include_router(category_router, prefix="/api/v1/category", tags=["Category"], dependencies=[Depends(JWTBearer())])
app.include_router(product_router,  prefix="/api/v1/product",  tags=["Product"],  dependencies=[Depends(JWTBearer())])
app.include_router(order_router,    prefix="/api/v1/order",    tags=["Order"],    dependencies=[Depends(JWTBearer())])
app.include_router(test_router,     prefix="/api/v1/test",     tags=["Test"],     dependencies=[Depends(JWTBearer())])
