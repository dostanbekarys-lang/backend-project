# app/services/auth_service.py
from sqlmodel import select
from app.models.user import User
from app.core.security import hash_password, verify_password, create_access_token, create_refresh_token

def register(session, email, password, tenant_id):
    user = session.exec(select(User).where(User.email == email)).first()
    if user: raise Exception("exists")

    user = User(
        email=email,
        password_hash=hash_password(password),
        tenant_id=tenant_id
    )
    session.add(user)
    session.commit()
    return user

def login(session, email, password):
    user = session.exec(select(User).where(User.email == email)).first()
    if not user or not verify_password(password, user.password_hash):
        raise Exception("invalid")

    return {
        "access": create_access_token({"sub": str(user.id), "role": user.role, "tenant": str(user.tenant_id)}),
        "refresh": create_refresh_token({"sub": str(user.id)})
    }