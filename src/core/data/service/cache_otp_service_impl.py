from typing import Optional, Dict

from loguru import logger

from src.core.domain.service.cache_otp_service import CacheOtpService

from ..external_service.redis_client import RedisMethod


class CacheOtpServiceImpl(CacheOtpService):
    def __init__(self, redis_method: RedisMethod):
        self._redis_method = redis_method

    async def check_and_increment_limit(self, email: str) -> bool:
        key = f"otp_limit:{email}"

        async with self._redis_method.pipeline(transaction=True) as pipe:
            res = await (pipe.incr(key).expire(key, 900).execute())

        current_count = res[0]
        return current_count < 5

    async def save_signup_otp(self, email: str, otp: str, name: str, password: str) -> None:
        key = f"signup_otp:{email}"
        data = {
            "otp": otp,
            "name": name,
            "password": password,
            "email": email
        }
        await self._redis_method.set_json(key, data, expire_seconds=600)

    async def verify_signup_otp(self, email: str, otp: str) -> Optional[Dict]:
        key = f"signup_otp:{email}"

        data = await self._redis_method.get_json(key)

        if not data or data["otp"] != otp:
            return None

        await self._redis_method.delete(key)
        await self._redis_method.delete(f"otp_limit:{email}")

        return data

    async def save_forgot_otp(self, email: str, otp: str, user_id: str) -> None:
        key = f"forgot_otp:{email}"
        data = {
            "otp": otp,
            "user_id": user_id
        }
        await self._redis_method.set_json(key, data, expire_seconds=600)

    async def verify_forgot_otp(self, email: str, otp: str) -> Optional[Dict]:
        key = f"forgot_otp:{email}"

        data = await self._redis_method.get_json(key)

        if not data or data["otp"] != otp:
            return None

        await self._redis_method.delete(key)
        await self._redis_method.delete(f"otp_limit:{email}")

        return data

    async def update_otp(self, email: str, otp: str) -> bool:
        signup_key = f"signup_otp:{email}"
        forgot_key = f"forgot_otp:{email}"

        signup_data = await self._redis_method.get_json(signup_key)
        if signup_data:
            signup_data["otp"] = otp
            await self._redis_method.set_json(signup_key, signup_data, expire_seconds=600)
            return True

        forgot_data = await self._redis_method.get_json(forgot_key)
        if forgot_data:
            forgot_data["otp"] = otp
            await self._redis_method.set_json(forgot_key, forgot_data, expire_seconds=600)
            return True

        return False
