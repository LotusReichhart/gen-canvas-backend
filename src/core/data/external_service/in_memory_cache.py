import asyncio
from typing import Any, Callable, Awaitable
from loguru import logger

class InMemoryCache:
    def __init__(self):
        self._cache: dict[str, Any] = {}
        self._locks: dict[str, asyncio.Lock] = {}

    async def _get_lock(self, key: str) -> asyncio.Lock:
        if key not in self._locks:
            self._locks[key] = asyncio.Lock()
        return self._locks[key]

    async def get(self, key: str) -> Any:
        return self._cache.get(key)

    async def set(self, key: str, value: Any):
        async with await self._get_lock(key):
            self._cache[key] = value

    async def get_or_set_atomic(
            self,
            key: str,
            async_factory_func: Callable[[], Awaitable[Any]]
    ) -> Any:
        value = self._cache.get(key)
        if value:
            return value

        lock = await self._get_lock(key)
        async with lock:
            value = self._cache.get(key)
            if value:
                return value

            logger.info(f"Cache miss for key '{key}'. Fetching data...")
            try:
                value = await async_factory_func()
                if value:
                    self._cache[key] = value
                return value
            except Exception as e:
                logger.error(f"Failed to populate cache for key '{key}': {e}")
                return None