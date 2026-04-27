# app/core/security.py
from datetime import datetime, timedelta
from jose import jwt
from passlib.context import CryptContext
from app.core.config import settings

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(p): return pwd_context.hash(p)
def verify_password(p, h): return pwd_context.verify(p, h)

def create_token(data, expires):
    payload = data.copy()
    payload["exp"] = datetime.utcnow() + expires
    return jwt.encode(payload, settings.SECRET_KEY, algorithm="HS256")

def create_access_token(data):
    return create_token(data, timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES))

def create_refresh_token(data):
    return create_token(data, timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS))