from fastapi             import FastAPI, Depends
from fastapi.staticfiles import StaticFiles
from core.middlewares    import setup_middlewares
from core.utils          import lifespan
from core.jwt_handler    import JWTBearer
from routers.user        import router as user_router
from routers.test        import router as test_router
from routers.category    import router as category_router
from routers.product     import router as product_router
from routers.order       import router as order_router

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
# sudo lsof -t -i tcp:8000 | xargs kill -9
# cd Desktop/backend/fastapi && venv\Scripts\activate
# eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6MSwicm9sZSI6ImFkbWluIiwiZXhwaXJ5IjoxNzMzNDA4MzA3fQ.vcX_KteifYsO5qDL9Qbs_3z4x66RYO-v6mJn2Cm9ZKs