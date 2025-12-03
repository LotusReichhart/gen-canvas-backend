from typing import Optional

from loguru import logger
from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.model.user.user_credit import UserCredit
from src.core.domain.repository.user_credit_repository import UserCreditRepository

from ..database.base_repository import BaseRepository
from ..database.model.user_credit_entity import UserCreditEntity
from ..mapper.user_credit_mapper import UserCreditMapper


class UserCreditRepositoryImpl(BaseRepository[UserCreditEntity], UserCreditRepository):
    def __init__(self, session: AsyncSession):
        super().__init__(model=UserCreditEntity, session=session)

    async def create_user_credit(self, user_credit: UserCredit) -> UserCredit:
        try:
            credit_entity = UserCreditMapper.to_entity(user_credit)
            credit_entity = await self.add(credit_entity)

            logger.info(f"Created credit account for User ID: {credit_entity.user_id}")

            return UserCreditMapper.to_model(credit_entity)
        except SQLAlchemyError as e:
            logger.error(f"Error creating user credit: {e}")
            raise

    async def get_user_credit_by_user_id(self, user_id: int) -> Optional[UserCredit]:
        try:
            query = select(UserCreditEntity).where(UserCreditEntity.user_id == user_id)
            result = await self.session.execute(query)
            credit_entity = result.scalar_one_or_none()

            if not credit_entity:
                return None

            return UserCreditMapper.to_model(credit_entity)
        except SQLAlchemyError as e:
            logger.error(f"Error fetching credit for user_id {user_id}: {e}")
            raise

    async def update_user_credit(self, user_credit: UserCredit) -> Optional[UserCredit]:
        if user_credit.id is None:
            logger.warning("Attempted to update credit account without ID")
            return None

        try:
            credit_entity = await self.get_by_id(user_credit.id)

            if not credit_entity:
                logger.warning(f"Credit update failed: Credit ID {credit_entity.id} not found")
                return None

            UserCreditMapper.to_update_entity(entity=credit_entity, user_credit=user_credit)

            await self.session.flush()
            await self.session.refresh(credit_entity)

            logger.info(f"Updated credit balance for User ID {credit_entity.user_id}: {credit_entity.balance}")

            return UserCreditMapper.to_model(credit_entity)

        except SQLAlchemyError as e:
            logger.error(f"Error updating credit account: {e}")
            raise
