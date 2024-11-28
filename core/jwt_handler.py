from fastapi          import Request, HTTPException
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from core.utils       import get_timestamp
from core.settings    import settings
import bcrypt
import jwt

def signJWT(id: int):
    return jwt.encode(
        payload   = {"id": id, "expiry": settings.jwt_expiry}, 
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

def hash_password(password: str):
    return bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode()

def check_password(password1: str, password2: str):
    try:
        return bcrypt.checkpw(password1.encode("utf-8"), password2.encode("utf-8"))
    except:
        return False

class JWTBearer(HTTPBearer):
    def __init__(self, auto_error: bool = True):
        super(JWTBearer, self).__init__(auto_error=auto_error)
    async def __call__(self, request: Request):
        credentials: HTTPAuthorizationCredentials = await super(JWTBearer, self).__call__(request)
        if not credentials.scheme == "Bearer":
            raise HTTPException(status_code=403, detail="Invalid authentication scheme.")
        if not self.verify_jwt(credentials.credentials):
            raise HTTPException(status_code=403, detail="Invalid or expired token.")
        return credentials.credentials
    def verify_jwt(self, jwtoken: str) -> bool:
        isTokenValid: bool = False
        try:
            payload = decodeJWT(jwtoken)
        except: 
            payload = None
        if payload: 
            isTokenValid = True
        return isTokenValid