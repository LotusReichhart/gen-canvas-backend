from loguru import logger
from typing import List

from src.core.common.constants import MsgKey
from src.core.common.exceptions import BusinessException

from ...dto.banner_dto import BannerResponse
from ...repository.unit_of_work import UnitOfWork


class GetListBannerUseCase:
    def __init__(self,
                 unit_of_work: UnitOfWork):
        self._uow = unit_of_work

    async def execute(self) -> List[BannerResponse]:
        try:
            async with self._uow as uow:
                banners = await uow.banner_repository.list_active_banners()

            return [BannerResponse.model_validate(b) for b in banners]
        except BusinessException:
            raise

        except Exception as e:
            logger.exception(f"GetListBannerUseCase error {e}")

            raise BusinessException(
                message_key=MsgKey.SERVER_ERROR,
                status_code=500
            )
