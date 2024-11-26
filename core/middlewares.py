from fastapi                   import FastAPI
from fastapi.middleware.cors   import CORSMiddleware
from starlette.middleware.base import BaseHTTPMiddleware
from http                      import HTTPStatus
import logging

class LogMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request, call_next):
        response    = await call_next(request)
        method      = request.method                                       # POST
        url_path    = str(request.url).replace(str(request.base_url), '/') # /api/v1/category/
        status_code = response.status_code                                 # 404
        code_desc   = HTTPStatus(status_code).phrase                       # Not Found
        msg         = f"{method} {url_path} {status_code} {code_desc}"
        if "200 OK" in msg:
            logging.info(msg)
        else:
            logging.error(msg)
        return response

def setup_middlewares(app: FastAPI):
    # app.add_middleware(LogMiddleware)
    app.add_middleware(
        middleware_class=CORSMiddleware,
        allow_origins=["https://localhost:8000", "https://www.localhost:8000"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )