from sqlmodel import create_engine, Session
from app.core.config import settings


engine = create_engine(
    settings.DATABASE_URL,
    echo=True,
    pool_pre_ping=True,
    pool_size=10,
    max_overflow=20
)


def get_session():
    with Session(engine) as session:
        yield session