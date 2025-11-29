from abc import ABC, abstractmethod

from src.core.model.user.user_credit import UserCredit


class UserCreditRepository(ABC):
    @abstractmethod
    async def create_user_credit(self, user_credit: UserCredit) -> UserCredit:
        """
        Tạo một tài khoản credit mới cho user
        """
        raise NotImplementedError

    @abstractmethod
    async def get_user_credit_by_user_id(self, user_id: int) -> UserCredit | None:
        """
        Lấy tài khoản credit (và số dư) bằng user_id.
        """
        raise NotImplementedError

    @abstractmethod
    async def update_user_credit(self, user_credit: UserCredit) -> UserCredit | None:
        """
        Cập nhật tài khoản credit.
        """
        raise NotImplementedError

