import redis
from app.core.config import settings

redis_client = redis.from_url(settings.REDIS_URL, decode_responses=True)


def get_redis():
    return redis_client


def cache_set(key: str, value: str, expire: int = 30):
    redis_client.setex(key, expire, value)


def cache_get(key: str) -> str | None:
    return redis_client.get(key)