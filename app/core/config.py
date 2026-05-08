from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    DATABASE_URL: str
    SECRET_KEY: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7
    REDIS_URL: str = "redis://redis:6379/0"
    CORS_ORIGINS: str = "http://localhost:3000,http://localhost:8000"

    SMTP_HOST: str = "smtp.gmail.com"
    SMTP_PORT: int = 587
    SMTP_USERNAME: str = ""
    SMTP_PASSWORD: str = ""
    EMAIL_FROM: str = ""
    APP_BASE_URL: str = "http://localhost:8000"

    ADMIN_EMAIL: str = "admin@test.com"
    ADMIN_PASSWORD: str = "admin123"

    class Config:
        env_file = ".env"


settings = Settings()

if not settings.SECRET_KEY:
    raise ValueError("SECRET_KEY is missing")