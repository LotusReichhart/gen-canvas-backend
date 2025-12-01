from loguru import logger

from src.core.common.constants import MsgKey
from src.core.common.exceptions import BusinessException

from ...repository.unit_of_work import UnitOfWork
from ...service.cache_token_service import CacheTokenService


class SignOutUseCase:
    def __init__(self,
                 unit_of_work: UnitOfWork,
                 cache_token_service: CacheTokenService):
        self._uow = unit_of_work
        self._cache_token_service = cache_token_service

    async def execute(self, user_id: int, signin_count: int, sign_out_count: int) -> None:
        try:
            async with self._uow as uow:
                user = await uow.user_repository.get_user_by_id(user_id=user_id)

                if not user:
                    raise BusinessException(
                        message_key=MsgKey.AUTH_REQUIRED,
                        status_code=401
                    )

                if (user.signin_count != signin_count
                        or user.sign_out_count != sign_out_count):
                    logger.warning(f"SignOut: Token out of sync for user {user_id}. Force clearing tokens.")
                    await self._cache_token_service.delete_all_refresh_tokens(user_id)

                    raise BusinessException(
                        message_key=MsgKey.AUTH_REQUIRED,
                        status_code=401
                    )

                user.increase_sign_out_count()
                await uow.user_repository.update_user(user)

            await self._cache_token_service.delete_all_refresh_tokens(user_id=user.id)

        except BusinessException:
            raise

        except Exception as e:
            logger.exception(f"SignOutUseCase error for user {e}")

            raise BusinessException(
                message_key=MsgKey.SERVER_ERROR,
                status_code=500
            )
