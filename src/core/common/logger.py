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

        if settings.ENV == "dev":
            logger.add(
                sys.stderr,
                level="DEBUG",
                format=log_format,
                colorize=True,
                backtrace=True,
                diagnose=True
            )
        else:
            logger.add(
                sys.stderr,
                level="ERROR",
                format=log_format,
                colorize=False
            )

            logger.add(
                "logs/app_{time:YYYY-MM-DD}.log",
                rotation="1 day",
                retention="10 days",
                level="INFO",
                encoding="utf-8"
            )

def setup_logging():
    AppLogger.setup()