from dependency_injector import containers, providers

from src.core.domain.service.ad_mob_verification_service import AdMobVerificationService
from src.core.domain.service.cache_otp_service import CacheOtpService
from src.core.domain.service.cache_token_service import CacheTokenService
from src.core.domain.service.mail_service import MailService
from src.core.domain.service.password_hasher_service import PasswordHasherService
from src.core.domain.service.storage_service import StorageService
from src.core.domain.service.token_service import TokenService

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

    cache_otp_service: CacheOtpService = providers.Singleton(
        CacheOtpServiceImpl,
        redis_method=external_service_container.redis_method
    )

    cache_token_service: CacheTokenService = providers.Singleton(
        CacheTokenServiceImpl,
        redis_method=external_service_container.redis_method,
        refresh_token_lifetime_seconds=config.REFRESH_TOKEN_LIFETIME
    )

    mail_service: MailService = providers.Factory(
        MailServiceImpl,
        transporter=external_service_container.mail_transporter
    )

    storage_service: StorageService = providers.Factory(
        StorageServiceImpl,
        client=external_service_container.s3_client,
        bucket_name=config.AWS_S3_BUCKET_NAME,
        region=config.AWS_S3_REGION
    )

    password_hasher_service: PasswordHasherService = providers.Factory(PasswordHasherServiceImpl)

    generate_otp_service = providers.Factory(GenerateOtpServiceImpl)

    token_service: TokenService = providers.Factory(
        TokenServiceImpl,
        access_secret=config.JWT_ACCESS_SECRET,
        refresh_secret=config.JWT_REFRESH_SECRET,
        access_lifetime=config.ACCESS_TOKEN_LIFETIME,
        refresh_lifetime=config.REFRESH_TOKEN_LIFETIME
    )

    admob_verification_service: AdMobVerificationService = providers.Factory(
        AdMobVerificationServiceImpl,
        cache=external_service_container.in_memory_cache,
        public_key_url=config.ADMOB_PUBLIC_KEY_URL
    )
