from dependency_injector import containers, providers

from ..in_memory_cache import InMemoryCache
from ..redis_client import RedisClient, RedisMethod
from ..mail_transporter import MailTransporter
from ..aws_s3_client import init_s3_client


class ExternalServiceContainer(containers.DeclarativeContainer):
    config = providers.Configuration()

    redis_client = providers.Singleton(
        RedisClient,
        url=config.REDIS_URL
    )

    redis_method = providers.Singleton(
        RedisMethod,
        client=redis_client.provided.client
    )

    mail_transporter = providers.Singleton(
        MailTransporter,
        host=config.MAIL_HOST,
        port=config.MAIL_PORT,
        user=config.MAIL_USER,
        password=config.MAIL_PASSWORD,
        sender=config.MAIL_SENDER_NAME
    )

    s3_client = providers.Resource(
        init_s3_client,
        aws_access_key_id=config.AWS_ACCESS_KEY_ID,
        aws_secret_access_key=config.AWS_SECRET_ACCESS_KEY,
        region_name=config.AWS_S3_REGION
    )

    in_memory_cache = providers.Singleton(InMemoryCache)