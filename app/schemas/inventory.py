from pydantic import BaseModel, Field


class InventoryCreateRequest(BaseModel):
    product_name: str
    location: str
    quantity: int = Field(ge=0)
    price: float = Field(ge=0)


class InventoryTransferRequest(BaseModel):
    product: str
    from_loc: str
    to_loc: str
    qty: int = Field(gt=0)


class DeadStockDecayRequest(BaseModel):
    discount_percent: float = Field(gt=0, le=90)