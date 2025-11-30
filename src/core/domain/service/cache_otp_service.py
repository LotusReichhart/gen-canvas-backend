from abc import ABC, abstractmethod
from typing import Optional, Dict


class CacheOtpService(ABC):
    @abstractmethod
    async def check_and_increment_limit(self, email: str) -> bool:
        raise NotImplementedError

    @abstractmethod
    async def save_signup_otp(self, email: str, otp: str, name: str, password: str) -> None:
        raise NotImplementedError

    @abstractmethod
    async def save_forgot_otp(self, email: str, otp: str, user_id: int) -> None:
        raise NotImplementedError

    @abstractmethod
    async def verify_signup_otp(self, email: str, otp: str) -> Optional[Dict]:
        raise NotImplementedError

    @abstractmethod
    async def verify_forgot_otp(self, email: str, otp: str) -> Optional[Dict]:
        raise NotImplementedError

    @abstractmethod
    async def update_otp(self, email: str, otp: str) -> bool:
        raise NotImplementedError
