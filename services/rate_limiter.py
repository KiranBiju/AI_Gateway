from fastapi import HTTPException
from app.core.redis_client import redis_client

RATE_LIMIT = 100
WINDOW = 60


def check_rate_limit(api_key: str):
    key = f"rate_limit:{api_key}"

    count = redis_client.incr(key)

    if count == 1:
        redis_client.expire(key, WINDOW)

    if count > RATE_LIMIT:
        raise HTTPException(
            status_code=429,
            detail="Rate limit exceeded"
        )