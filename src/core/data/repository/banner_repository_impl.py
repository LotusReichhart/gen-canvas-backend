from typing import List

from loguru import logger
from sqlalchemy import asc, select
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.model.user.banner import Banner
from src.core.domain.repository.banner_repository import BannerRepository

from ..database.base_repository import BaseRepository
from ..database.model.banner_entity import BannerEntity
from ..mapper.banner_mapper import BannerMapper


class BannerRepositoryImpl(BaseRepository[BannerEntity], BannerRepository):
    def __init__(self, session: AsyncSession):
        super().__init__(model=BannerEntity, session=session)

    async def list_active_banners(self) -> List[Banner]:
        try:
            stmt = (
                select(BannerEntity)
                .where(BannerEntity.is_active == True)
                .order_by(asc(BannerEntity.display_order))
            )

            result = await self.session.execute(stmt)
            banner_models = result.scalars().all()

            return [
                BannerMapper.to_model(model)
                for model in banner_models
            ]
        except SQLAlchemyError as e:
            logger.exception(f"Error fetching active banners: {e}")
            raise
