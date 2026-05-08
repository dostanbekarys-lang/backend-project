import uuid
from sqlmodel import SQLModel, Field


class User(SQLModel, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    email: str = Field(unique=True, index=True)
    password_hash: str
    role: str = Field(default="user")
    tenant_id: uuid.UUID = Field(index=True)
    is_verified: bool = Field(default=False)