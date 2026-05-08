from fastapi import APIRouter, Depends, Header, HTTPException, Query
from jose import jwt, JWTError
from sqlmodel import Session

from app.core.config import settings
from app.core.database import get_session
from app.schemas.inventory import (
    InventoryCreateRequest,
    InventoryTransferRequest,
    DeadStockDecayRequest,
)
from app.services.inventory_service import (
    create_inventory,
    list_inventory,
    transfer,
    run_dead_stock_decay,
)
from app.worker import send_email_task


router = APIRouter(
    prefix="/inventory",
    tags=["Inventory"]
)


def get_current_user(authorization: str = Header(None)):
    if not authorization:
        raise HTTPException(status_code=401, detail="Authorization header missing")

    if not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Invalid authorization format")

    token = authorization.replace("Bearer ", "")

    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")

    return payload


def require_verified_user(user: dict):
    tenant_id = user.get("tenant_id")

    if not tenant_id:
        raise HTTPException(status_code=401, detail="Tenant not found in token")

    return tenant_id


@router.post("/create")
def create_item(
    data: InventoryCreateRequest,
    session: Session = Depends(get_session),
    user=Depends(get_current_user)
):
    tenant_id = require_verified_user(user)

    return create_inventory(
        session=session,
        tenant_id=tenant_id,
        product_name=data.product_name,
        location=data.location,
        quantity=data.quantity,
        price=data.price
    )


@router.get("/list")
def get_inventory(
    limit: int = Query(default=20, ge=1, le=100),
    offset: int = Query(default=0, ge=0),
    session: Session = Depends(get_session),
    user=Depends(get_current_user)
):
    tenant_id = require_verified_user(user)
    return list_inventory(session, tenant_id, limit, offset)


@router.post("/transfer")
def transfer_inventory(
    data: InventoryTransferRequest,
    session: Session = Depends(get_session),
    user=Depends(get_current_user)
):
    tenant_id = require_verified_user(user)

    result = transfer(
        session=session,
        tenant_id=tenant_id,
        product=data.product,
        from_loc=data.from_loc,
        to_loc=data.to_loc,
        qty=data.qty
    )

    send_email_task.delay(
        user.get("email"),
        "LeanStock Inventory Transfer",
        f"Transfer completed: {data.qty} {data.product} from {data.from_loc} to {data.to_loc}."
    )

    return result


@router.post("/decay/run")
def dead_stock_decay(
    data: DeadStockDecayRequest,
    session: Session = Depends(get_session),
    user=Depends(get_current_user)
):
    tenant_id = require_verified_user(user)

    result = run_dead_stock_decay(
        session=session,
        tenant_id=tenant_id,
        discount_percent=data.discount_percent
    )

    send_email_task.delay(
        user.get("email"),
        "LeanStock Dead Stock Decay",
        f"Dead stock decay applied with discount {data.discount_percent}%."
    )

    return result