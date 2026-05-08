import uuid
from datetime import datetime
from sqlmodel import SQLModel, Field


class Inventory(SQLModel, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)

    tenant_id: uuid.UUID = Field(index=True)
    product_name: str = Field(index=True)
    location: str = Field(index=True)

    quantity: int = Field(default=0)
    price: float = Field(default=0)

    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)