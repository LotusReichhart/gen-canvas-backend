from typing import Optional
from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession
from loguru import logger
from sqlalchemy.orm import selectinload

from src.core.model.user.user import User

from src.core.domain.repository.user_repository import UserRepository

from ..database.base_repository import BaseRepository
from ..database.model.user_entity import UserEntity
from ..mapper.user_mapper import UserMapper


class UserRepositoryImpl(BaseRepository[UserEntity], UserRepository):
    def __init__(self, session: AsyncSession):
        super().__init__(model=UserEntity, session=session)

    async def get_user_by_id(self, user_id: int) -> Optional[User]:
        try:
            query = (
                select(UserEntity)
                .options(selectinload(UserEntity.user_credit))
                .where(UserEntity.id == user_id)
            )

            result = await self.session.execute(query)
            user_entity = result.scalar_one_or_none()

            if not user_entity:
                return None

            return UserMapper.to_model(user_entity)

        except SQLAlchemyError as e:
            logger.error(f"Error fetching user by id {e}")
            raise

    async def get_user_by_email(self, email: str) -> Optional[User]:
        try:
            query = select(UserEntity).where(UserEntity.email == email)
            result = await self.session.execute(query)
            user_entity = result.scalar_one_or_none()

            if not user_entity:
                return None

            return UserMapper.to_model(user_entity)

        except SQLAlchemyError as e:
            logger.error(f"Error fetching user by email {e}")
            raise

    async def exists_by_email(self, email: str) -> bool:
        try:
            query = select(1).where(UserEntity.email == email)
            result = await self.session.execute(query)
            exists = result.scalar() is not None

            if exists:
                logger.debug(f"Checked email existence: {email} -> Exists")
            return exists

        except SQLAlchemyError as e:
            logger.error(f"Error checking email existence {e}")
            raise

    async def create_user(self, user: User) -> User:
        try:
            user_entity = UserMapper.to_entity(user)
            created_entity = await self.add(user_entity)

            logger.info(f"User created successfully: ID={created_entity.id}, Email={created_entity.email}")

            return UserMapper.to_model(created_entity)

        except SQLAlchemyError as e:
            logger.error(f"Error creating user {e}")
            raise

    async def update_user(self, user: User) -> User | None:
        if user.id is None:
            logger.warning("Attempted to update user without ID")
            return None

        try:
            query = (
                select(UserEntity)
                .options(selectinload(UserEntity.user_credit))
                .where(UserEntity.id == user.id)
            )
            result = await self.session.execute(query)
            user_entity = result.scalar_one_or_none()

            if not user_entity:
                logger.warning(f"User update failed: User ID {user.id} not found")
                return None

            UserMapper.to_update_entity(entity=user_entity, user=user)

            await self.session.flush()
            await self.session.refresh(user_entity)

            logger.info(f"User updated successfully: ID={user.id}")

            return UserMapper.to_model(user_entity)

        except SQLAlchemyError as e:
            logger.error(f"Error updating user ID {e}")
            raise
