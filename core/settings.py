from pydantic   import BaseModel
from typing     import List
from core.utils import get_timestamp
import os


class Settings(BaseModel):
    # cors
    allow_origins: List  = [
        "http://localhost:8000", 
        "http://www.localhost:8000"
    ]
    # jwt
    jwt_key:       str   = os.getenv("KEY", "xyz")
    jwt_algorithm: str   = "HS256"
    jwt_expiry:    int = get_timestamp() + 60 * 60 * 168 # 168 hours = 1 week


settings = Settings()