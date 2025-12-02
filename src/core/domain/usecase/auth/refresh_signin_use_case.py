from typing import Dict

from loguru import logger

from src.core.common.constants import MsgKey
from src.core.common.exceptions import BusinessException

from ...repository.unit_of_work import UnitOfWork
from ...service.cache_token_service import CacheTokenService
from ...service.token_service import TokenService


class RefreshSigninUseCase:
    def __init__(self,
                 unit_of_work: UnitOfWork,
                 token_service: TokenService,
                 cache_token_service: CacheTokenService):
        self._uow = unit_of_work
        self._token_service = token_service
        self._cache_token_service = cache_token_service

    async def execute(self, refresh_token: str) -> Dict[str, str]:
        try:
            try:
                payload = self._token_service.verify_refresh_token(token=refresh_token)
                if not payload:
                    raise Exception("Token verification returned None")
            except Exception as e:
                logger.warning(f"Invalid refresh token signature/expiry: {e}")
                raise BusinessException(
                    message_key=MsgKey.AUTH_REQUIRED,
                    status_code=401
                )

            user_id = payload["id"]
            device_id = payload["jti"]
            signin_count = payload["signin_count"]
            sign_out_count = payload["sign_out_count"]

            async with self._uow as uow:
                user = await uow.user_repository.get_user_by_id(user_id=user_id)

            if not user:
                raise BusinessException(
                    message_key=MsgKey.USER_NOT_FOUND,
                    status_code=401
                )

            if (
                    user.signin_count != signin_count
                    or user.sign_out_count != sign_out_count
            ):
                logger.warning(f"Token out of sync for user {user_id}. Possible reused token.")

                await self._cache_token_service.delete_all_refresh_tokens(user_id)
                raise BusinessException(
                    message_key=MsgKey.AUTH_REQUIRED,
                    status_code=401
                )

            stored_hash = await self._cache_token_service.get_refresh_token_hash(user_id, device_id)
            current_token_hash = self._cache_token_service.hash_token(refresh_token)

            if not stored_hash or current_token_hash != stored_hash:
                logger.error(f"Refresh Token Mismatch (Breach Detected) for user {user_id}")
                await self._cache_token_service.delete_all_refresh_tokens(user_id)
                raise BusinessException(
                    message_key=MsgKey.AUTH_REQUIRED,
                    status_code=401
                )

            access_token_data = self._token_service.create_access_token(
                user_id=user.id,
                signin_count=signin_count,
                sign_out_count=sign_out_count,
                refresh_jti=device_id
            )
            access_token = access_token_data["token"]

            return {"access_token": access_token}

        except BusinessException:
            raise

        except Exception as e:
            logger.error(f"RefreshSigninUseCase error")

            raise BusinessException(
                message_key=MsgKey.SERVER_ERROR,
                status_code=500
            )
