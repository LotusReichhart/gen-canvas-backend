from loguru import logger
from typing import Any

from src.core.common.constants import MsgKey
from src.core.common.exceptions import BusinessException
from src.core.common.logger import setup_logging

from ...repository.user_repository import UserRepository

setup_logging()


class GetUserProfileUseCase:
    def __init__(self,
                 user_repository: UserRepository):
        self.user_repository = user_repository

    async def execute(self, user_id: int) -> dict[str, Any]:
        try:
            user = await self.user_repository.get_user_by_id(user_id)
            if not user:
                raise BusinessException(
                    message_key=MsgKey.USER_NOT_FOUND,
                    status_code=404
                )
            return {"user": user, "credit": user.credit_account}
        except BusinessException:
            raise

        except Exception as e:
            logger.exception(f"GetUserProfileUseCase: {e}")
            raise BusinessException(
                message_key=MsgKey.SERVER_ERROR,
                status_code=500
            )
