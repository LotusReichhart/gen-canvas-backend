import secrets

from src.core.domain.service.generate_otp_service import GenerateOtpService


class GenerateOtpServiceImpl(GenerateOtpService):
    def generate_otp(self, length: int = 6) -> str:
        return ''.join(str(secrets.randbelow(10)) for _ in range(length))
