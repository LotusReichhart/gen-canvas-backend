from typing import Self
from loguru import logger

from src.core.domain.repository.unit_of_work import UnitOfWork

from src.core.data.database.postgres import PostgresDatabase

from .banner_repository_impl import BannerRepositoryImpl
from .credit_transaction_repository_impl import CreditTransactionRepositoryImpl
from .user_credit_repository_impl import UserCreditRepositoryImpl
from .user_repository_impl import UserRepositoryImpl


class UnitOfWorkImpl(UnitOfWork):
    def __init__(self, db: PostgresDatabase):
        self._session_factory = db.session_factory
        self._session = None

    async def __aenter__(self) -> Self:
        self._session = self._session_factory()

        self.user_repository = UserRepositoryImpl(self._session)
        self.user_credit_repository = UserCreditRepositoryImpl(self._session)
        self.credit_transaction_repository = CreditTransactionRepositoryImpl(self._session)
        self.banner_repository = BannerRepositoryImpl(self._session)

        return self

    async def __aexit__(self, exc_type, exc_val, traceback):
        if exc_type:
            logger.error(f"UnitOfWork Transaction Failed: {exc_val}")
            await self.rollback()
        else:
            await self.commit()

        await self._session.close()

    async def commit(self):
        try:
            await self._session.commit()
        except Exception as e:
            logger.exception("Commit failed, rolling back.")
            await self.rollback()
            raise e

    async def rollback(self):
        await self._session.rollback()
