from typing import List
from loguru import logger
from sqlalchemy import select, desc
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.domain.repository.credit_transaction_repository import CreditTransactionRepository
from src.core.model.user.credit_transaction import CreditTransaction

from ..database.base_repository import BaseRepository
from ..database.model.credit_transaction_entity import CreditTransactionEntity
from ..database.model.user_credit_entity import UserCreditEntity
from ..mapper.credit_transaction_mapper import CreditTransactionMapper


class CreditTransactionRepositoryImpl(BaseRepository[CreditTransactionEntity], CreditTransactionRepository):
    def __init__(self, session: AsyncSession):
        super().__init__(model=CreditTransactionEntity, session=session)

    async def create_transaction(self, transaction: CreditTransaction) -> CreditTransaction:
        try:
            transaction_entity = CreditTransactionMapper.to_entity(transaction)
            created_entity = await self.add(transaction_entity)
            logger.info(
                f"Created credit transaction ID: {created_entity.id} for CreditAccount ID: {created_entity.credit_id}")

            return CreditTransactionMapper.to_model(created_entity)
        except SQLAlchemyError as e:
            logger.error(f"Error creating credit transaction: {e}")
            raise

    async def list_transactions_by_user_id(
            self,
            user_id: int,
            limit: int = 20,
            offset: int = 0
    ) -> List[CreditTransaction]:
        try:
            stmt = (
                select(CreditTransactionEntity)
                .join(UserCreditEntity, CreditTransactionEntity.credit_id == UserCreditEntity.id)
                .where(UserCreditEntity.user_id == user_id)
                .order_by(desc(CreditTransactionEntity.created_at))
                .limit(limit)
                .offset(offset)
            )

            result = await self.session.execute(stmt)
            transaction_models = result.scalars().all()

            return [
                CreditTransactionMapper.to_model(model)
                for model in transaction_models
            ]

        except SQLAlchemyError as e:
            logger.error(f"Error listing transactions for user {user_id}: {e}")
            raise


