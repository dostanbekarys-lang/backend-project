# app/models/inventory.py
from sqlmodel import SQLModel, Field
import uuid

class Inventory(SQLModel, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    tenant_id: uuid.UUID
    product_name: str
    location: str
    quantity: int
    price: float