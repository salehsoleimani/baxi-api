from redis.asyncio import ConnectionPool
from redis.asyncio.client import Redis

from app.config.config import settings

redis_connection_pool = ConnectionPool.from_url(url=settings.REDIS_URL, max_connections=100, decode_responses=True)


async def get_redis() -> Redis:
    redis = Redis(connection_pool=redis_connection_pool)
    return redis
