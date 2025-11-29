from abc import ABC, abstractmethod
from typing import Any


class AdMobVerificationService(ABC):
    @abstractmethod
    async def verify_reward_webhook(self, query_params: dict[str, Any]) -> bool:
        raise NotImplementedError
