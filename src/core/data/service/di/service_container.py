from dependency_injector import containers, providers

from ..ad_mob_verification_service_impl import AdMobVerificationServiceImpl
from ..cache_otp_service_impl import CacheOtpServiceImpl
from ..cache_token_service_impl import CacheTokenServiceImpl
from ..generate_otp_service_impl import GenerateOtpServiceImpl
from ..mail_service_impl import MailServiceImpl
from ..password_hasher_service_impl import PasswordHasherServiceImpl
from ..storage_service_impl import StorageServiceImpl
from ..token_service_impl import TokenServiceImpl


class ServiceContainer(containers.DeclarativeContainer):
    config = providers.Configuration()
    external_service_container = providers.DependenciesContainer()

    cache_otp_service = providers.Singleton(
        CacheOtpServiceImpl,
        redis_method=external_service_container.redis_method
    )

    cache_token_service = providers.Singleton(
        CacheTokenServiceImpl,
        redis_method=external_service_container.redis_method
    )

    mail_service = providers.Factory(
        MailServiceImpl,
        transporter=external_service_container.mail_transporter
    )

    storage_service = providers.Factory(
        StorageServiceImpl,
        client=external_service_container.s3_client,
        bucket_name=config.AWS_S3_BUCKET_NAME,
        region=config.AWS_S3_REGION
    )

    password_hasher_service = providers.Factory(PasswordHasherServiceImpl)

    generate_otp_service = providers.Factory(GenerateOtpServiceImpl)

    token_service = providers.Factory(
        TokenServiceImpl,
        access_secret=config.JWT_ACCESS_SECRET,
        refresh_secret=config.JWT_REFRESH_SECRET,
        access_lifetime=config.ACCESS_TOKEN_LIFETIME,
        refresh_lifetime=config.REFRESH_TOKEN_LIFETIME
    )

    admob_verification_service = providers.Factory(
        AdMobVerificationServiceImpl,
        cache=external_service_container.in_memory_cache,
        public_key_url=config.ADMOB_PUBLIC_KEY_URL
    )