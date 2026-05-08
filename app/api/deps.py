from fastapi import Depends, HTTPException
from jose import jwt
from app.core.config import settings

def get_user(token: str):
    try:
        return jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
    except:
        raise HTTPException(401)

def require_role(role):
    def inner(user=Depends(get_user)):
        if user["role"] != role:
            raise HTTPException(403)
        return user
    return inner