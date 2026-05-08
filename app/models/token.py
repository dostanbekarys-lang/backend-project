import uuid
from datetime import datetime
from sqlmodel import SQLModel, Field


class RefreshToken(SQLModel, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    user_id: uuid.UUID = Field(index=True)
    token: str = Field(index=True)
    revoked: bool = Field(default=False)
    created_at: datetime = Field(default_factory=datetime.utcnow)


class EmailVerificationToken(SQLModel, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    user_id: uuid.UUID = Field(index=True)
    token: str = Field(index=True)
    used: bool = Field(default=False)
    created_at: datetime = Field(default_factory=datetime.utcnow)


class PasswordResetToken(SQLModel, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    user_id: uuid.UUID = Field(index=True)
    token: str = Field(index=True)
    used: bool = Field(default=False)
    created_at: datetime = Field(default_factory=datetime.utcnow)