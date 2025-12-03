from typing import Dict

from loguru import logger

from src.core.common.constants import MsgKey
from src.core.common.exceptions import BusinessException

from ...repository.unit_of_work import UnitOfWork
from ...service.cache_otp_service import CacheOtpService
from ...service.generate_otp_service import GenerateOtpService
from ...service.mail_service import MailService


class RequestForgotPasswordUseCase:
    def __init__(self,
                 unit_of_work: UnitOfWork,
                 generate_otp_service: GenerateOtpService,
                 cache_otp_service: CacheOtpService,
                 mail_service: MailService):
        self._uow = unit_of_work
        self._generate_otp_service = generate_otp_service
        self._cache_otp_service = cache_otp_service
        self._mail_service = mail_service

    async def execute(self, email: str, lang: str = "en") -> None:

        async with self._uow as uow:
            user = await uow.user_repository.get_user_by_email(email)

            if not user:
                raise BusinessException(
                    message_key=MsgKey.VALIDATION_ERROR,
                    status_code=400,
                    error_details={"email": MsgKey.EMAIL_NOT_FOUND}
                )

            user_id = user.id
        try:
            allowed = await self._cache_otp_service.check_and_increment_limit(email)

            if not allowed:
                raise BusinessException(
                    message_key=MsgKey.SPAM_DETECTED,
                    status_code=429
                )

            otp = self._generate_otp_service.generate_otp()
            template = self._mail_service.build_otp_template(otp=otp, lang=lang)
            await self._mail_service.send_mail(
                to=email,
                subject=template["subject"],
                html=template["html"],
            )

            await self._cache_otp_service.save_forgot_otp(email=email, otp=otp, user_id=user_id)
        except BusinessException:
            raise

        except Exception as e:
            logger.error(f"RequestForgotPasswordUseCase error for email {e}")

            raise BusinessException(
                message_key=MsgKey.SERVER_ERROR,
                status_code=500
            )
