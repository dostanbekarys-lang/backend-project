# app/models/user.py
from sqlmodel import SQLModel, Field
import uuid

class User(SQLModel, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    email: str = Field(unique=True, index=True)
    password_hash: str
    role: str = "user"
    tenant_id: uuid.UUID