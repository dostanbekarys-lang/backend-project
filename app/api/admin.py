from fastapi import APIRouter, Depends, Header, HTTPException
from jose import jwt, JWTError
from sqlmodel import Session, select

from app.core.config import settings
from app.core.database import get_session
from app.models.user import User


router = APIRouter(
    prefix="/admin",
    tags=["Admin"]
)


def get_admin_user(authorization: str = Header(None)):
    if not authorization:
        raise HTTPException(status_code=401, detail="Authorization header missing")

    if not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Invalid authorization format")

    token = authorization.replace("Bearer ", "")

    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")

    if payload.get("role") != "admin":
        raise HTTPException(status_code=403, detail="Admin role required")

    return payload


@router.get("/users")
def list_users(
    session: Session = Depends(get_session),
    admin=Depends(get_admin_user)
):
    users = session.exec(select(User)).all()

    return [
        {
            "id": str(user.id),
            "email": user.email,
            "role": user.role,
            "tenant_id": str(user.tenant_id),
            "is_verified": user.is_verified
        }
        for user in users
    ]