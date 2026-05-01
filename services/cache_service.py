import json
from app.core.redis_client import redis_client


def get_cache(key: str):
    data = redis_client.get(key)
    if data:
        return json.loads(data)
    return None


def set_cache(key: str, value: dict, ttl: int = 600):
    redis_client.setex(key, ttl, json.dumps(value))