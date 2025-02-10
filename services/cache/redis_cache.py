from redis.asyncio import Redis, ConnectionPool
from settings import settings


class AsyncRedisCache:
    def __init__(self, namespace: str):
        pool = ConnectionPool.from_url(url=settings.redis_url)
        self.redis = Redis.from_pool(connection_pool=pool)
        self.namespace = namespace

    async def set_value(self, key: str, value: str, expire: int = settings.time_in_cache) -> None:
        await self.redis.set(f"{self.namespace}:{key}", value, ex=expire)

    async def get_value(self, key: str) -> str:
        if value := await self.redis.get(f"{self.namespace}:{key}"):
            return value
