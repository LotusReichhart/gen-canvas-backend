from typing import Dict

from loguru import logger
from datetime import datetime, timezone

from src.core.common.constants import MsgKey
from src.core.common.exceptions import BusinessException

from src.core.model.user.enums.auth_provider import AuthProvider
from src.core.model.user.enums.user_status import UserStatus
from src.core.model.user.enums.user_tier import UserTier
from src.core.model.user.user import User
from src.core.model.user.user_credit import UserCredit

from ...repository.unit_of_work import UnitOfWork
from ...service.cache_otp_service import CacheOtpService
from ...service.cache_token_service import CacheTokenService
from ...service.token_service import TokenService


class SignupVerificationUseCase:
    def __init__(self,
                 unit_of_work: UnitOfWork,
                 cache_otp_service: CacheOtpService,
                 token_service: TokenService,
                 cache_token_service: CacheTokenService):
        self._uow = unit_of_work
        self._cache_otp_service = cache_otp_service
        self._token_service = token_service
        self._cache_token_service = cache_token_service

    async def execute(self, email: str, otp: str) -> Dict[str, str]:
        try:
            otp_data = await self._cache_otp_service.verify_signup_otp(email=email, otp=otp)
            if not otp_data:
                raise BusinessException(
                    message_key=MsgKey.VALIDATION_ERROR,
                    status_code=400,
                    error_details={"otp": MsgKey.INVALID_OTP}
                )

            current_time = datetime.now(timezone.utc)
            new_user = User(
                name=otp_data["name"],
                email=otp_data["email"],
                password=otp_data["password"],
                avatar=None,
                last_login=current_time,
                status=UserStatus.ACTIVE,
                tier=UserTier.FREE,
                auth_provider=AuthProvider.EMAIL
            )

            async with self._uow as uow:
                user = await uow.user_repository.create_user(new_user)

                new_user_credit = UserCredit(user_id=user.id, balance=5)
                await uow.user_credit_repository.create_user_credit(new_user_credit)

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
            logger.exception(f"SignupVerificationUseCase error for email {e}")
            raise BusinessException(
                message_key=MsgKey.SERVER_ERROR,
                status_code=500
            )
