from fastapi import APIRouter, Depends, Query, Request
from sqlmodel import Session

from app.core.database import get_session
from app.core.rate_limit import rate_limit
from app.schemas.auth import (
    RegisterRequest,
    LoginRequest,
    VerifyEmailRequest,
    RefreshRequest,
    LogoutRequest,
    PasswordResetRequest,
    PasswordResetConfirmRequest,
)
from app.services.auth_service import (
    register,
    verify_email,
    login,
    refresh,
    logout,
    request_password_reset,
    confirm_password_reset,
)


router = APIRouter(
    prefix="/auth",
    tags=["Auth"]
)


@router.post("/register")
def register_user(
    request: Request,
    data: RegisterRequest,
    session: Session = Depends(get_session)
):
    rate_limit(request.client.host, "register")
    return register(session, data.email, data.password)


@router.post("/verify-email")
def verify_email_post(
    data: VerifyEmailRequest,
    session: Session = Depends(get_session)
):
    return verify_email(session, data.token)


@router.get("/verify-email")
def verify_email_get(
    token: str = Query(...),
    session: Session = Depends(get_session)
):
    return verify_email(session, token)


@router.post("/login")
def login_user(
    request: Request,
    data: LoginRequest,
    session: Session = Depends(get_session)
):
    rate_limit(request.client.host, "login")
    return login(session, data.email, data.password)


@router.post("/refresh")
def refresh_token(
    data: RefreshRequest,
    session: Session = Depends(get_session)
):
    return refresh(session, data.refresh_token)


@router.post("/logout")
def logout_user(
    data: LogoutRequest,
    session: Session = Depends(get_session)
):
    return logout(session, data.refresh_token)


@router.post("/password-reset/request")
def password_reset_request(
    request: Request,
    data: PasswordResetRequest,
    session: Session = Depends(get_session)
):
    rate_limit(request.client.host, "password_reset")
    return request_password_reset(session, data.email)


@router.post("/password-reset/confirm")
def password_reset_confirm(
    data: PasswordResetConfirmRequest,
    session: Session = Depends(get_session)
):
    return confirm_password_reset(session, data.token, data.new_password)