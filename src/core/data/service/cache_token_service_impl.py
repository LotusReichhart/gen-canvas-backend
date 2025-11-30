from typing import Optional, Dict

from loguru import logger
import hashlib

from src.core.domain.service.cache_token_service import CacheTokenService

from ..external_service.redis_client import RedisMethod


class CacheTokenServiceImpl(CacheTokenService):
    def __init__(self,
                 redis_method: RedisMethod,
                 refresh_token_lifetime_seconds: int):
        self._redis_method = redis_method
        self._refresh_token_lifetime_seconds = refresh_token_lifetime_seconds

    def hash_token(self, token: str) -> str:
        return hashlib.sha256(token.encode()).hexdigest()

    async def save_refresh_token(self, user_id: int, device_id: str, token: str) -> None:
        key = f"user_sessions:{user_id}"
        hashed_token = self.hash_token(token)

        await self._redis_method.hset(key, device_id, hashed_token)
        await self._redis_method.expire(key, self._refresh_token_lifetime_seconds)

    async def get_refresh_token_hash(self, user_id: int, device_id: str) -> Optional[str]:
        key = f"user_sessions:{user_id}"
        hashed_token = await self._redis_method.hget(key, device_id)

        if hashed_token is None:
            return None

        if isinstance(hashed_token, bytes):
            return hashed_token.decode("utf-8")

        return hashed_token

    async def delete_refresh_token(self, user_id: int, device_id: str) -> None:
        key = f"user_sessions:{user_id}"
        await self._redis_method.hdel(key, device_id)

    async def delete_all_refresh_tokens(self, user_id: int) -> None:
        key = f"user_sessions:{user_id}"
        await self._redis_method.delete(key)
        logger.info(f"Deleted all sessions for user {user_id}")

    async def save_reset_token(self, token: str, user_id: str) -> None:
        hashed = self.hash_token(token)
        key = f"reset_token:{hashed}"
        data = {"user_id": user_id}
        await self._redis_method.set_json(key, data, expire_seconds=600)

    async def verify_reset_token(self, token: str) -> Optional[Dict]:
        hashed = self.hash_token(token)
        key = f"reset_token:{hashed}"

        data = await self._redis_method.get_json(key)
        if not data:
            return None

        await self.delete_reset_token(token)
        return data

    async def delete_reset_token(self, token: str) -> None:
        hashed = self.hash_token(token)
        await self._redis_method.delete(f"reset_token:{hashed}")
