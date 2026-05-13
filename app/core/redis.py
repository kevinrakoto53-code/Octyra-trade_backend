import redis
from app.core.config import settings

def get_redis_client():
    return redis.from_url(
        settings.REDIS_URL,
        decode_responses=True,
        socket_connect_timeout=5,
        socket_timeout=5,
        retry_on_timeout=True,
        health_check_interval=30,
    )

redis_client = get_redis_client()

def get_redis():
    return redis_client

def cache_set(key: str, value: str, expire: int = 30):
    try:
        redis_client.setex(key, expire, value)
    except Exception:
        pass

def cache_get(key: str) -> str | None:
    try:
        return redis_client.get(key)
    except Exception:
        return None