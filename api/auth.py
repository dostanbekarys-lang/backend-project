# app/api/auth.py
from fastapi import APIRouter, Depends, Request
from sqlmodel import Session
from app.core.database import get_session
from app.services.auth_service import register, login
from app.core.rate_limit import rate_limit

router = APIRouter(prefix="/auth")

@router.post("/register")
def reg(req: Request, email: str, password: str, session: Session = Depends(get_session)):
    rate_limit(req.client.host, "reg")
    return register(session, email, password, tenant_id="11111111-1111-1111-1111-111111111111")

@router.post("/login")
def log(req: Request, email: str, password: str, session: Session = Depends(get_session)):
    rate_limit(req.client.host, "log")
    return login(session, email, password)