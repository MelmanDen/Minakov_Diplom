import pytest
import os
import asyncio
from services.cache.redis_cache import AsyncRedisCache


@pytest.fixture()
def redis_client():
    redis_client = AsyncRedisCache(namespace="test")
    return redis_client


@pytest.fixture
def env():
    return os.getenv("REDIS_URL")


def test_redis_catch_env(env):
    assert env
    assert env == "redis://localhost:6379/0?decode_responses=True"


@pytest.mark.asyncio
async def test_redis_set_get_value(redis_client):
    await redis_client.set_value(key='key', value='value')
    result = await redis_client.get_value(key='key')
    assert result == 'value'


@pytest.mark.asyncio
async def test_redis_set_ex_value(redis_client):
    await redis_client.set_value('key', 'value', 1)
    result = await redis_client.get_value('key')
    assert result == 'value'
    await asyncio.sleep(2)
    result = await redis_client.get_value('key')
    assert result is None
