from typing import Dict

from loguru import logger
from datetime import datetime, timezone

from src.core.common.constants import MsgKey
from src.core.common.exceptions import BusinessException

from ...repository.unit_of_work import UnitOfWork
from ...service.cache_token_service import CacheTokenService
from ...service.password_hasher_service import PasswordHasherService
from ...service.token_service import TokenService



class SigninWithEmailUseCase:
    def __init__(self,
                 unit_of_work: UnitOfWork,
                 password_hasher_service: PasswordHasherService,
                 token_service: TokenService,
                 cache_token_service: CacheTokenService):
        self._uow = unit_of_work
        self._password_hasher_service = password_hasher_service
        self._token_service = token_service
        self._cache_token_service = cache_token_service

    async def execute(self, email: str, password: str) -> Dict[str, str]:
        try:
            async with self._uow as uow:
                user = await uow.user_repository.get_user_by_email(email)

                if not user:
                    raise BusinessException(
                        message_key=MsgKey.VALIDATION_ERROR,
                        status_code=400,
                        error_details={"email": MsgKey.EMAIL_NOT_FOUND}
                    )

                is_verify = self._password_hasher_service.verify(
                    hashed_password=user.password,
                    password=password
                )

                if not is_verify:
                    raise BusinessException(
                        message_key=MsgKey.VALIDATION_ERROR,
                        status_code=400,
                        error_details={"password": MsgKey.WRONG_PASSWORD}
                    )

                user.last_login = datetime.now(timezone.utc)
                user.increase_signin_count()

                await uow.user_repository.update_user(user)

            refresh_token_data = self._token_service.create_refresh_token(
                user_id=user.id,
                signin_count=user.signin_count,
                sign_out_count=user.sign_out_count
            )
            refresh_token = refresh_token_data["token"]
            device_id = refresh_token_data["device_id"]

            access_token_data = self._token_service.create_access_token(
                user_id=user.id,
                signin_count=user.signin_count,
                sign_out_count=user.sign_out_count,
                refresh_jti=device_id
            )
            access_token = access_token_data["token"]

            await self._cache_token_service.save_refresh_token(
                user_id=user.id,
                device_id=device_id,
                token=refresh_token
            )

            return {
                "access_token": access_token,
                "refresh_token": refresh_token
            }

        except BusinessException:
            raise

        except Exception as e:
            logger.exception(f"Error during Signin for email: {e}")
            raise BusinessException(
                message_key=MsgKey.SERVER_ERROR,
                status_code=500
            )
