from abc import ABC, abstractmethod
from typing import Self

from .banner_repository import BannerRepository
from .credit_transaction_repository import CreditTransactionRepository
from .user_credit_repository import UserCreditRepository
from .user_repository import UserRepository


class UnitOfWork(ABC):
    user_repository: UserRepository
    credit_repository: UserCreditRepository
    credit_transaction_repository: CreditTransactionRepository
    banner_repository: BannerRepository

    @abstractmethod
    async def __aenter__(self) -> Self:
        """Bắt đầu một UoW context."""
        raise NotImplementedError

    @abstractmethod
    async def __aexit__(self, exc_type, exc_val, traceback):
        """Kết thúc UoW context (commit hoặc rollback)."""
        raise NotImplementedError

    @abstractmethod
    async def commit(self):
        """Commit transaction."""
        raise NotImplementedError

    @abstractmethod
    async def rollback(self):
        """Rollback transaction."""
        raise NotImplementedError