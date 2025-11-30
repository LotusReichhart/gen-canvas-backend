from argon2.exceptions import VerifyMismatchError
from loguru import logger

from argon2 import PasswordHasher

from src.core.domain.service.password_hasher_service import PasswordHasherService


class PasswordHasherServiceImpl(PasswordHasherService):
    def __init__(self):
        self.ph = PasswordHasher()

    def hash(self, password: str) -> str:
        return self.ph.hash(password)

    def verify(self, hashed_password: str, password: str) -> bool:
        try:
            return self.ph.verify(hashed_password, password)
        except VerifyMismatchError as e:
            logger.exception(f"Password verification VerifyMismatchError: {e}")
            return False
        except Exception as e:
            logger.exception(f"Password verification failed with unexpected error: {e}")
            return False
