from abc import ABC, abstractmethod
from typing import List

from src.core.model.user.credit_transaction import CreditTransaction


class CreditTransactionRepository(ABC):
    @abstractmethod
    async def create_transaction(self, transaction: CreditTransaction) -> CreditTransaction:
        """
        Ghi lại một giao dịch (lịch sử) credit mới vào CSDL.
        """
        raise NotImplementedError

    @abstractmethod
    async def list_transactions_by_user_id(
            self,
            user_id: int,
            limit: int = 20,
            offset: int = 0
    ) -> List[CreditTransaction]:
        """
        Lấy danh sách lịch sử giao dịch của một user, có phân trang.
        """
        raise NotImplementedError
