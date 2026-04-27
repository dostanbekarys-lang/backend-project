# app/services/inventory_service.py
from sqlmodel import select
from app.models.inventory import Inventory

def transfer(session, tenant_id, product, from_loc, to_loc, qty):

    from_inv = session.exec(
        select(Inventory).where(
            Inventory.product_name == product,
            Inventory.location == from_loc,
            Inventory.tenant_id == tenant_id
        )
    ).first()

    to_inv = session.exec(
        select(Inventory).where(
            Inventory.product_name == product,
            Inventory.location == to_loc,
            Inventory.tenant_id == tenant_id
        )
    ).first()

    if from_inv.quantity < qty:
        raise Exception("no stock")

    from_inv.quantity -= qty
    to_inv.quantity += qty

    session.commit()