import json
from typing import Optional, Union

import redis.asyncio as redis
from loguru import logger


class RedisClient:
    def __init__(self, url: str):
        self.client = redis.from_url(
            url,
            encoding="utf-8",
            decode_responses=True,
        )

    async def get_client(self) -> redis.Redis:
        return self.client

    async def close(self):
        await self.client.close()
        logger.info("Redis connection closed")

    async def ping(self):
        try:
            await self.client.ping()
            logger.info("Connected to Redis successfully")
        except Exception as e:
            logger.error(f"Failed to connect to Redis: {e}")
            raise


class RedisMethod:
    def __init__(self, client: redis.Redis):
        self.client = client

    async def set_json(self, key: str, data: dict, expire_seconds: int | None = None):
        value = json.dumps(data)
        await self.client.set(key, value, ex=expire_seconds)

    async def get_json(self, key: str) -> Optional[dict]:
        value = await self.client.get(key)
        return json.loads(value) if value else None

    async def set(self, key: str, value: Union[str, int, dict], expire_seconds: int | None = None):
        if isinstance(value, dict):
            value = json.dumps(value)
        else:
            value = str(value)
        await self.client.set(key, value, ex=expire_seconds)

    async def get(self, key: str) -> Optional[str]:
        return await self.client.get(key)

    async def delete(self, *keys: str):
        if keys:
            await self.client.delete(*keys)

    async def incr(self, key: str) -> int:
        return await self.client.incr(key)

    async def hset(self, key: str, field: str, value: str):
        await self.client.hset(key, field, value)

    async def hget(self, key: str, field: str) -> bytes | None:
        return await self.client.hget(key, field)

    async def hdel(self, key: str, field: str):
        await self.client.hdel(key, field)

    async def expire(self, key: str, seconds: int):
        await self.client.expire(key, seconds)

    async def exists(self, key: str) -> bool:
        return await self.client.exists(key) == 1

    def pipeline(self, transaction: bool = True):
        return self.client.pipeline(transaction=transaction)

    def scan_iter(self, match: str):
        return self.client.scan_iter(match=match)
