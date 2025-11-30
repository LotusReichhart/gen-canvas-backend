from abc import ABC, abstractmethod
from typing import Dict


class MailService(ABC):
    @abstractmethod
    async def send_mail(self, to: str, subject: str, html: str) -> bool:
        raise NotImplementedError

    @abstractmethod
    def build_otp_template(self, otp: str) -> Dict[str, str]:
        raise NotImplementedError
