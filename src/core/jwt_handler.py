from fastapi           import Request, HTTPException
from fastapi.security  import HTTPAuthorizationCredentials, HTTPBearer

from src.core.utils    import get_timestamp
from src.core.settings import settings

import bcrypt
import jwt

def signJWT(id: int, role: str) -> str:
    return jwt.encode(
        payload   = {
            "id":     id, 
            "role":   role,
            "expiry": settings.jwt_expiry
        }, 
        key       = settings.jwt_key, 
        algorithm = settings.jwt_algorithm
    )

def decodeJWT(token: str) -> dict:
    try:
        decoded: dict = jwt.decode(
            jwt        = token, 
            key        = settings.jwt_key, 
            algorithms = [settings.jwt_algorithm]
        )
        return decoded if decoded["expiry"] >= get_timestamp() else None
    except:
        return {}

def hash_password(password: str) -> str:
    return bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode()

def check_password(password1: str, password2: str) -> bool:
    try:
        return bcrypt.checkpw(password1.encode("utf-8"), password2.encode("utf-8"))
    except:
        return False

class JWTBearer(HTTPBearer):
    def __init__(self, auto_error: bool = True, role: str = "admin"):
        super(JWTBearer, self).__init__(auto_error=auto_error)
        self.role = role
    async def __call__(self, request: Request):
        token: HTTPAuthorizationCredentials = await super(JWTBearer, self).__call__(request)
        if not token.scheme == "Bearer":
            raise HTTPException(status_code=403, detail="Invalid authentication scheme.")
        if not self.verify_jwt(token.credentials):
            raise HTTPException(status_code=403, detail="Invalid or expired token.")
        if not self.has_required_role(token.credentials, self.role):
            raise HTTPException(status_code=403, detail="Invalid or expired token.")
        return token.credentials
    def verify_jwt(self, token: str) -> bool:
        try:
            payload = decodeJWT(token)
        except:
            payload = None
        return payload is not None
    def has_required_role(self, token: str, role: str) -> bool:
        try:
            payload = decodeJWT(token)
            user_role = payload.get("role", "")
            return user_role == role or user_role == "admin"
        except Exception:
            return False
