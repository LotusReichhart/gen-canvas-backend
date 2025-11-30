from loguru import logger

from src.core.common.constants import MsgKey
from src.core.common.exceptions import BusinessException

from ...repository.user_repository import UserRepository
from ...service.cache_otp_service import CacheOtpService
from ...service.generate_otp_service import GenerateOtpService
from ...service.mail_service import MailService
from ...service.password_hasher_service import PasswordHasherService


class RequestSignupUseCase:
    def __init__(self,
                 user_repository: UserRepository,
                 generate_otp_service: GenerateOtpService,
                 cache_otp_service: CacheOtpService,
                 mail_service: MailService,
                 password_hasher_service: PasswordHasherService):
        self._user_repository = user_repository
        self._generate_otp_service = generate_otp_service
        self._cache_otp_service = cache_otp_service
        self._mail_service = mail_service
        self._password_hasher_service = password_hasher_service

    async def execute(self, email: str, name: str, password: str) -> dict[str, str]:
        existing_user = await self._user_repository.exists_by_email(email)
        if existing_user:
            raise BusinessException(
                message_key=MsgKey.VALIDATION_ERROR,
                status_code=400,
                error_details={"email": MsgKey.EMAIL_EXISTS}
            )

        try:
            allowed = await self._cache_otp_service.check_and_increment_limit(email)

            if not allowed:
                raise BusinessException(
                    message_key=MsgKey.SPAM_DETECTED,
                    status_code=429
                )

            otp = self._generate_otp_service.generate_otp()
            template = self._mail_service.build_otp_template(otp)
            await self._mail_service.send_mail(
                to=email,
                subject=template["subject"],
                html=template["html"],
            )

            hashed_pw = self._password_hasher_service.hash(password)
            await self._cache_otp_service.save_signup_otp(
                email=email,
                otp=otp,
                name=name,
                password=hashed_pw
            )

            return {"email": email}

        except BusinessException:
            raise

        except Exception as e:
            logger.exception(f"RequestSignupUseCase unexpected error for email {e}")
            raise BusinessException(
                message_key=MsgKey.SERVER_ERROR,
                status_code=500
            )
