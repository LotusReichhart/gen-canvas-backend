from typing import Dict

from loguru import logger
from datetime import datetime, timezone

from google.oauth2 import id_token
from google.auth.transport import requests

from src.core.common.constants import MsgKey
from src.core.common.exceptions import BusinessException

from src.core.model.user.user import User
from src.core.model.user.enums.auth_provider import AuthProvider
from src.core.model.user.enums.user_status import UserStatus
from src.core.model.user.enums.user_tier import UserTier
from src.core.model.user.user_credit import UserCredit

from ...repository.unit_of_work import UnitOfWork
from ...service.cache_token_service import CacheTokenService
from ...service.token_service import TokenService


class SignInWithGoogleUseCase:
    def __init__(self,
                 unit_of_work: UnitOfWork,
                 token_service: TokenService,
                 cache_token_service: CacheTokenService,
                 client_id: str):
        self._uow = unit_of_work
        self._token_service = token_service
        self._cache_token_service = cache_token_service
        self._client_id = client_id

    async def execute(self, user_id_token: str) -> Dict[str, str]:
        try:
            idinfo = id_token.verify_oauth2_token(
                user_id_token, requests.Request(), self._client_id
            )

            user_email = idinfo.get("email")
            if not user_email:
                logger.warning("Google Token verified but missing email")
                raise BusinessException(
                    message_key=MsgKey.INVALID_TOKEN,
                    status_code=400
                )

        except ValueError as e:
            logger.warning(f"Google verify failed: {e}")
            raise BusinessException(
                message_key=MsgKey.GOOGLE_AUTH_FAILED,
                status_code=401
            )
        except Exception as e:
            logger.error("Unexpected error during Google Verification")
            raise BusinessException(message_key=MsgKey.SERVER_ERROR, status_code=500)

        try:
            async with self._uow as uow:
                user = await uow.user_repository.get_user_by_email(email=user_email)

                if not user:
                    current_time = datetime.now(timezone.utc)
                    new_user = User(
                        id=None,
                        name=idinfo.get("name"),
                        email=user_email,
                        avatar=idinfo.get("picture"),
                        last_login=current_time,
                        status=UserStatus.ACTIVE,
                        tier=UserTier.FREE,
                        auth_provider=AuthProvider.GOOGLE
                    )

                    user = await uow.user_repository.create_user(new_user)

                    new_user_credit = UserCredit(user_id=user.id, balance=5)
                    await uow.credit_repository.create_user_credit(new_user_credit)

                    logger.info(f"New Google user created: {user_email}")

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
            logger.error(
                f"Error handling Google Auth for email: {user_email if 'user_email' in locals() else 'unknown'}")
            raise BusinessException(
                message_key=MsgKey.SERVER_ERROR,
                status_code=500
            )
