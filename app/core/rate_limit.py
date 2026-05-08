import redis
from fastapi import HTTPException
from app.core.config import settings


redis_client = redis.Redis.from_url(settings.REDIS_URL)


def rate_limit(ip: str, key: str, limit: int = 5, seconds: int = 60):
    redis_key = f"rate_limit:{key}:{ip}"

    current = redis_client.get(redis_key)

    if current and int(current) >= limit:
        raise HTTPException(
            status_code=429,
            detail="Too many requests. Try again later."
        )

    redis_client.incr(redis_key)
    redis_client.expire(redis_key, seconds)