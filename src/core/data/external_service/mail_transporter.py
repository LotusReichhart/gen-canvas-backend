import aiosmtplib
from email.mime.text import MIMEText
from loguru import logger

class MailTransporter:
    def __init__(
        self,
        host: str,
        port: int,
        user: str,
        password: str,
        sender: str
    ):
        self.host = host
        self.port = port
        self.user = user
        self.password = password
        self.sender = sender

    async def send(self, to: str, subject: str, html: str) -> bool:
        message = MIMEText(html, "html")
        message["From"] = self.sender
        message["To"] = to
        message["Subject"] = subject

        try:
            await aiosmtplib.send(
                message,
                hostname=self.host,
                port=self.port,
                username=self.user,
                password=self.password,
                start_tls=True,
            )
            logger.info(f"Email sent to {to}")
            return True
        except Exception as e:
            logger.error(f"MailTransporter Error: {e}")
            return False