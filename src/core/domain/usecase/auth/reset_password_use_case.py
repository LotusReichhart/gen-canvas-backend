from loguru import logger

from src.core.common.constants import MsgKey
from src.core.common.exceptions import BusinessException
from src.core.common.logger import setup_logging

from ...repository.unit_of_work import UnitOfWork
from ...service.cache_token_service import CacheTokenService
from ...service.password_hasher_service import PasswordHasherService

setup_logging()


class ResetPasswordUseCase:
    def __init__(self,
                 unit_of_work: UnitOfWork,
                 cache_token_service: CacheTokenService,
                 password_hasher_service: PasswordHasherService):
        self._uow = unit_of_work
        self._cache_token_service = cache_token_service
        self._password_hasher_service = password_hasher_service

    async def execute(self, reset_token: str, new_password: str):
        try:
            token_data = await self._cache_token_service.verify_reset_token(reset_token)
            if not token_data or not token_data.get("user_id"):
                raise BusinessException(
                    message_key=MsgKey.FORBIDDEN,
                    status_code=403
                )

            user_id = int(token_data.get("user_id"))

            async with self._uow as uow:
                user = await uow.user_repository.get_user_by_id(user_id)
                if not user:
                    raise BusinessException(
                        message_key=MsgKey.USER_NOT_FOUND,
                        status_code=404
                    )

                hashed_pw = self._password_hasher_service.hash(new_password)
                user.password = hashed_pw

                await uow.user_repository.update_user(user)

        except BusinessException:
            raise

        except Exception as e:
            logger.exception(f"ResetPasswordUseCase error for token {e}")

            raise BusinessException(
                message_key=MsgKey.SERVER_ERROR,
                status_code=500
            )
