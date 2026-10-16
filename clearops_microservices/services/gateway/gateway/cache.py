import os

import redis.asyncio as redis

TTL_SECONDS = int(os.getenv("CACHE_TTL_SECONDS", "30"))
_client = redis.from_url(os.environ["REDIS_URL"]) if os.getenv("REDIS_URL") else None


async def get(key: str) -> bytes | None:
    try:
        return await _client.get(key) if _client else None
    except redis.RedisError:
        return None


async def put(key: str, value: bytes) -> None:
    try:
        if _client:
            await _client.set(key, value, ex=TTL_SECONDS)
    except redis.RedisError:
        pass


async def invalidate(prefix: str) -> None:
    try:
        if _client:
            async for k in _client.scan_iter(f"{prefix}*"):
                await _client.delete(k)
    except redis.RedisError:
        pass
