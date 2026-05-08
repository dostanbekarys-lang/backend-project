import uuid
from datetime import datetime
from fastapi import HTTPException
from sqlmodel import select, Session
from app.models.inventory import Inventory


def create_inventory(session: Session, tenant_id, product_name, location, quantity, price):
    item = Inventory(
        tenant_id=uuid.UUID(str(tenant_id)),
        product_name=product_name,
        location=location,
        quantity=quantity,
        price=price,
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow()
    )

    session.add(item)
    session.commit()
    session.refresh(item)

    return {
        "message": "Inventory item created",
        "id": str(item.id),
        "product_name": item.product_name,
        "location": item.location,
        "quantity": item.quantity,
        "price": item.price,
        "tenant_id": str(item.tenant_id)
    }


def list_inventory(session: Session, tenant_id, limit: int = 20, offset: int = 0):
    items = session.exec(
        select(Inventory)
        .where(Inventory.tenant_id == uuid.UUID(str(tenant_id)))
        .offset(offset)
        .limit(limit)
    ).all()

    return items


def transfer(session: Session, tenant_id, product, from_loc, to_loc, qty):
    tenant_uuid = uuid.UUID(str(tenant_id))

    from_inv = session.exec(
        select(Inventory).where(
            Inventory.product_name == product,
            Inventory.location == from_loc,
            Inventory.tenant_id == tenant_uuid
        )
    ).first()

    if not from_inv:
        raise HTTPException(
            status_code=404,
            detail="Source inventory not found"
        )

    to_inv = session.exec(
        select(Inventory).where(
            Inventory.product_name == product,
            Inventory.location == to_loc,
            Inventory.tenant_id == tenant_uuid
        )
    ).first()

    if not to_inv:
        raise HTTPException(
            status_code=404,
            detail="Destination inventory not found"
        )

    if from_inv.quantity < qty:
        raise HTTPException(
            status_code=400,
            detail="Not enough stock"
        )

    from_inv.quantity -= qty
    to_inv.quantity += qty

    from_inv.updated_at = datetime.utcnow()
    to_inv.updated_at = datetime.utcnow()

    session.add(from_inv)
    session.add(to_inv)
    session.commit()

    return {
        "message": "Transfer successful",
        "product": product,
        "from_location": from_loc,
        "to_location": to_loc,
        "transferred_quantity": qty,
        "from_remaining": from_inv.quantity,
        "to_total": to_inv.quantity
    }


def run_dead_stock_decay(session: Session, tenant_id, discount_percent: float):
    tenant_uuid = uuid.UUID(str(tenant_id))

    items = session.exec(
        select(Inventory).where(
            Inventory.tenant_id == tenant_uuid,
            Inventory.quantity > 0
        )
    ).all()

    updated_items = []

    for item in items:
        old_price = item.price
        item.price = round(item.price * (1 - discount_percent / 100), 2)
        item.updated_at = datetime.utcnow()

        session.add(item)

        updated_items.append({
            "product_name": item.product_name,
            "location": item.location,
            "old_price": old_price,
            "new_price": item.price
        })

    session.commit()

    return {
        "message": "Dead stock decay applied",
        "discount_percent": discount_percent,
        "updated_count": len(updated_items),
        "items": updated_items
    }