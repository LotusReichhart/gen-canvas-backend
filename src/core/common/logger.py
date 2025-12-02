import sys
from loguru import logger

from src.config import settings


class AppLogger:
    @staticmethod
    def setup():
        logger.remove()

        log_format = (
            "<green>{time:YYYY-MM-DD HH:mm:ss}</green> | "
            "<level>{level: <8}</level> | "
            "<cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - <level>{message}</level>"
        )

        sink = sys.stdout

        if settings.ENV == "development":
            logger.add(
                sink,
                level="DEBUG",
                format=log_format,
                colorize=True,
                backtrace=True,
                diagnose=True,
                enqueue=True
            )
        else:
            logger.add(
                sys.stdout,
                level="ERROR",
                format=log_format,
                colorize=False,
                enqueue=True
            )

            logger.add(
                "logs/app_{time:YYYY-MM-DD}.log",
                rotation="1 day",
                retention="10 days",
                level="INFO",
                encoding="utf-8"
            )

        logger.info(f"Logger setup complete. ENV: {settings.ENV}")

def setup_logging():
    AppLogger.setup()