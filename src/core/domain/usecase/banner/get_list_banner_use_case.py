from loguru import logger
from typing import List

from src.core.common.constants import MsgKey
from src.core.common.exceptions import BusinessException
from src.core.model.user.banner import Banner

from ...repository.banner_repository import BannerRepository


class GetListBannerUseCase:
    def __init__(self,
                 banner_repository: BannerRepository):
        self.banner_repository = banner_repository

    async def execute(self) -> dict[str, List[Banner]]:
        try:
            banners = await self.banner_repository.list_active_banners()
            return {"banners": banners}
        except BusinessException:
            raise

        except Exception as e:
            logger.exception(f"GetListBannerUseCase error {e}")

            raise BusinessException(
                message_key=MsgKey.SERVER_ERROR,
                status_code=500
            )
