from abc import ABC, abstractmethod
from typing import Optional, Dict


class CacheTokenService(ABC):
    @abstractmethod
    def hash_token(self, token: str) -> str:
        raise NotImplementedError

    @abstractmethod
    async def save_refresh_token(self, user_id: int, device_id: str, token: str) -> None:
        raise NotImplementedError

    @abstractmethod
    async def get_refresh_token_hash(self, user_id: int, device_id: str) -> Optional[str]:
        raise NotImplementedError

    @abstractmethod
    async def delete_refresh_token(self, user_id: int, device_id: str) -> None:
        raise NotImplementedError

    @abstractmethod
    async def delete_all_refresh_tokens(self, user_id: int) -> None:
        raise NotImplementedError

    @abstractmethod
    async def save_reset_token(self, token: str, user_id: str) -> None:
        raise NotImplementedError

    @abstractmethod
    async def verify_reset_token(self, token: str) -> Optional[Dict]:
        raise NotImplementedError

    @abstractmethod
    async def delete_reset_token(self, token: str) -> None:
        raise NotImplementedError
