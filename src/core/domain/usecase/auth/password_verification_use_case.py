from typing import Dict

from loguru import logger

from src.core.common.constants import MsgKey
from src.core.common.exceptions import BusinessException

from ...service.cache_otp_service import CacheOtpService
from ...service.cache_token_service import CacheTokenService
from ...service.token_service import TokenService

class PasswordVerificationUseCase:
    def __init__(self,
                 token_service: TokenService,
                 cache_otp_service: CacheOtpService,
                 cache_token_service: CacheTokenService):
        self._token_service = token_service
        self._cache_otp_service = cache_otp_service
        self._cache_token_service = cache_token_service

    async def execute(self, email: str, otp: str) -> Dict[str, str]:
        try:
            otp_data = await self._cache_otp_service.verify_forgot_otp(email=email, otp=otp)
            if not otp_data:
                raise BusinessException(
                    message_key=MsgKey.VALIDATION_ERROR,
                    status_code=400,
                    error_details={"otp": MsgKey.INVALID_OTP}
                )

            user_id = otp_data["user_id"]

            reset_token = self._token_service.create_reset_token()

            await self._cache_token_service.save_reset_token(
                token=reset_token,
                user_id=user_id
            )

            return {"reset_token": reset_token}

        except BusinessException:
            raise

        except Exception as e:
            logger.exception(f"PasswordVerificationUseCase error for email {e}")

            raise BusinessException(
                message_key=MsgKey.SERVER_ERROR,
                status_code=500
            )
