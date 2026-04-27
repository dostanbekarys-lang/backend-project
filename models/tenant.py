# app/models/tenant.py
from sqlmodel import SQLModel, Field
import uuid

class Tenant(SQLModel, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    name: str