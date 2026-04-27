# app/core/rate_limit.py
import redis
from fastapi import HTTPException
from app.core.config import settings

r = redis.Redis.from_url(settings.REDIS_URL)

def rate_limit(ip: str, key: str):
    k = f"{key}:{ip}"
    val = r.get(k)
    if val and int(val) >= 5:
        raise HTTPException(429, "Too many requests")
    r.incr(k)
    r.expire(k, 60)