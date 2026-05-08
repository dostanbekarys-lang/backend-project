import uuid
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlmodel import SQLModel, Session, select

from app.core.config import settings
from app.core.database import engine
from app.core.security import hash_password

from app.api import auth, inventory, admin

from app.models.user import User
from app.models.inventory import Inventory
from app.models.token import (
    RefreshToken,
    EmailVerificationToken,
    PasswordResetToken,
)


app = FastAPI(
    title="LeanStock Backend",
    version="2.0.0",
    description="Production-grade inventory backend with JWT auth, email verification, Redis worker, PostgreSQL and multi-tenancy."
)


@app.on_event("startup")
def on_startup():
    SQLModel.metadata.create_all(engine)

    with Session(engine) as session:
        admin_user = session.exec(
            select(User).where(User.email == settings.ADMIN_EMAIL)
        ).first()

        if not admin_user:
            admin_user = User(
                email=settings.ADMIN_EMAIL,
                password_hash=hash_password(settings.ADMIN_PASSWORD),
                role="admin",
                tenant_id=uuid.UUID("11111111-1111-1111-1111-111111111111"),
                is_verified=True
            )

            session.add(admin_user)
            session.commit()


app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS.split(","),
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(auth.router)
app.include_router(inventory.router)
app.include_router(admin.router)


@app.get("/")
def root():
    return {
        "message": "LeanStock Backend API is running"
    }