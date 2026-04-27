# app/core/config.py
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    DATABASE_URL: str
    SECRET_KEY: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int
    REFRESH_TOKEN_EXPIRE_DAYS: int
    REDIS_URL: str
    CORS_ORIGINS: str

    class Config:
        env_file = ".env"

settings = Settings()

if not settings.SECRET_KEY:
    raise ValueError("SECRET_KEY missing")