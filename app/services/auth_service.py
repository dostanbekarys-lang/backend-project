import uuid
import secrets
from fastapi import HTTPException
from sqlmodel import select, Session

from app.models.user import User
from app.models.token import (
    RefreshToken,
    EmailVerificationToken,
    PasswordResetToken,
)
from app.core.security import (
    hash_password,
    verify_password,
    create_access_token,
    create_refresh_token,
)
from app.worker import send_email_task
from app.core.config import settings


DEFAULT_TENANT_ID = "11111111-1111-1111-1111-111111111111"


def register(session: Session, email: str, password: str):
    existing_user = session.exec(
        select(User).where(User.email == email)
    ).first()

    if existing_user:
        raise HTTPException(
            status_code=409,
            detail="User already exists"
        )

    user = User(
        email=email,
        password_hash=hash_password(password),
        role="user",
        tenant_id=uuid.UUID(DEFAULT_TENANT_ID),
        is_verified=False
    )

    session.add(user)
    session.commit()
    session.refresh(user)

    verification_token = secrets.token_urlsafe(32)

    token_row = EmailVerificationToken(
        user_id=user.id,
        token=verification_token
    )

    session.add(token_row)
    session.commit()

    verification_link = f"{settings.APP_BASE_URL}/auth/verify-email?token={verification_token}"

    email_body = f"""
Hello!

Thank you for registering in LeanStock.

Please verify your email using this link:

{verification_link}

Or copy this token and use it in Postman:

{verification_token}
"""

    send_email_task.delay(
        user.email,
        "LeanStock Email Verification",
        email_body
    )

    return {
        "message": "User registered successfully. Please verify your email.",
        "user_id": str(user.id),
        "email": user.email,
        "role": user.role,
        "is_verified": user.is_verified,
        "verification_token_for_demo": verification_token
    }


def verify_email(session: Session, token: str):
    token_row = session.exec(
        select(EmailVerificationToken).where(
            EmailVerificationToken.token == token,
            EmailVerificationToken.used == False
        )
    ).first()

    if not token_row:
        raise HTTPException(
            status_code=400,
            detail="Invalid or already used verification token"
        )

    user = session.get(User, token_row.user_id)

    if not user:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    user.is_verified = True
    token_row.used = True

    session.add(user)
    session.add(token_row)
    session.commit()

    return {
        "message": "Email verified successfully",
        "email": user.email,
        "is_verified": user.is_verified
    }


def login(session: Session, email: str, password: str):
    user = session.exec(
        select(User).where(User.email == email)
    ).first()

    if not user or not verify_password(password, user.password_hash):
        raise HTTPException(
            status_code=401,
            detail="Invalid email or password"
        )

    if not user.is_verified:
        raise HTTPException(
            status_code=403,
            detail="Email is not verified"
        )

    access_token = create_access_token({
        "sub": str(user.id),
        "email": user.email,
        "role": user.role,
        "tenant_id": str(user.tenant_id)
    })

    refresh_token = create_refresh_token({
        "sub": str(user.id)
    })

    refresh_row = RefreshToken(
        user_id=user.id,
        token=refresh_token,
        revoked=False
    )

    session.add(refresh_row)
    session.commit()

    return {
        "access": access_token,
        "refresh": refresh_token,
        "token_type": "bearer"
    }


def refresh(session: Session, refresh_token: str):
    token_row = session.exec(
        select(RefreshToken).where(
            RefreshToken.token == refresh_token,
            RefreshToken.revoked == False
        )
    ).first()

    if not token_row:
        raise HTTPException(
            status_code=401,
            detail="Invalid or revoked refresh token"
        )

    user = session.get(User, token_row.user_id)

    if not user:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    token_row.revoked = True

    new_access_token = create_access_token({
        "sub": str(user.id),
        "email": user.email,
        "role": user.role,
        "tenant_id": str(user.tenant_id)
    })

    new_refresh_token = create_refresh_token({
        "sub": str(user.id)
    })

    new_refresh_row = RefreshToken(
        user_id=user.id,
        token=new_refresh_token,
        revoked=False
    )

    session.add(token_row)
    session.add(new_refresh_row)
    session.commit()

    return {
        "access": new_access_token,
        "refresh": new_refresh_token,
        "token_type": "bearer"
    }


def logout(session: Session, refresh_token: str):
    token_row = session.exec(
        select(RefreshToken).where(
            RefreshToken.token == refresh_token,
            RefreshToken.revoked == False
        )
    ).first()

    if not token_row:
        raise HTTPException(
            status_code=401,
            detail="Invalid or already revoked refresh token"
        )

    token_row.revoked = True
    session.add(token_row)
    session.commit()

    return {
        "message": "Logged out successfully"
    }


def request_password_reset(session: Session, email: str):
    user = session.exec(
        select(User).where(User.email == email)
    ).first()

    if not user:
        return {
            "message": "If this email exists, password reset instructions were sent"
        }

    reset_token = secrets.token_urlsafe(32)

    reset_row = PasswordResetToken(
        user_id=user.id,
        token=reset_token,
        used=False
    )

    session.add(reset_row)
    session.commit()

    reset_link = f"{settings.APP_BASE_URL}/auth/password-reset/confirm?token={reset_token}"

    email_body = f"""
Hello!

You requested password reset for LeanStock.

Use this reset link:

{reset_link}

Or copy this token and use it in Postman:

{reset_token}
"""

    send_email_task.delay(
        user.email,
        "LeanStock Password Reset",
        email_body
    )

    return {
        "message": "If this email exists, password reset instructions were sent",
        "reset_token_for_demo": reset_token
    }


def confirm_password_reset(session: Session, token: str, new_password: str):
    token_row = session.exec(
        select(PasswordResetToken).where(
            PasswordResetToken.token == token,
            PasswordResetToken.used == False
        )
    ).first()

    if not token_row:
        raise HTTPException(
            status_code=400,
            detail="Invalid or already used reset token"
        )

    user = session.get(User, token_row.user_id)

    if not user:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    user.password_hash = hash_password(new_password)
    token_row.used = True

    session.add(user)
    session.add(token_row)
    session.commit()

    return {
        "message": "Password reset successfully"
    }