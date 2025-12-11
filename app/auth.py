from passlib.context import CryptContext
from datetime import datetime, timedelta
import jwt
from .config import settings

pwd_ctx = CryptContext(schemes=["argon2"], deprecated="auto")


def hash_password(password: str) -> str:
    return pwd_ctx.hash(password)

def verify_password(plain: str, hashed: str) -> bool:
    return pwd_ctx.verify(plain, hashed)

def create_access_token(data: dict, expires_delta: int | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + timedelta(seconds=expires_delta)
    else:
        expire = datetime.utcnow() + timedelta(seconds=settings.ACCESS_TOKEN_EXPIRE_SECONDS)
    to_encode.update({"exp": expire})
    token = jwt.encode(to_encode, settings.JWT_SECRET, algorithm=settings.JWT_ALGORITHM)
    return token

def decode_token(token: str):
    try:
        payload = jwt.decode(token, settings.JWT_SECRET, algorithms=[settings.JWT_ALGORITHM])
        return payload
    except jwt.ExpiredSignatureError:
        raise
    except Exception as e:
        raise
