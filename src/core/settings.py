from pydantic       import BaseModel
from typing         import List

from src.core.utils import get_timestamp

import os

class Settings(BaseModel):
    # admin
    admin_username: str = os.getenv("USERNAME", "admin")
    admin_password: str = os.getenv("PASSWORD", "123")
    # cors
    allow_origins: List = [
        "http://localhost:8000", 
        "http://www.localhost:8000"
    ]
    # jwt
    jwt_key: str = os.getenv("KEY", "xyz")
    jwt_algorithm: str = "HS256"
    jwt_expiry: int = get_timestamp() + 604800 # 604800=1 week | 2592000=1 month
    # swagger
    swagger_ui_parameters: dict = {
        "defaultModelsExpandDepth": -1,
    }

settings = Settings()
