from abc import ABC, abstractmethod
from datetime import date
from typing import Dict, Any

from src.core.model.user.user import UserTier


class UserCreditCalculatorService(ABC):
    @abstractmethod
    def calculate_refill(
            self,
            current_balance: int,
            last_refill_date: date,
            tier: UserTier
    ) -> Dict[str, Any]:
        raise NotImplementedError
