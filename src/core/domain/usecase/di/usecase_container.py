from dependency_injector import containers, providers

from ..user.get_user_profile_use_case import GetUserProfileUseCase


class UseCaseContainer(containers.DeclarativeContainer):
    repository_container = providers.DependenciesContainer()
    external_service_container = providers.DependenciesContainer()

    # --- Auth Use Cases ---

    # request_signup_use_case = providers.Factory(
    #     "src.core.domain.usecases.request_signup.RequestSignupUseCase",
    #     # Inject Repository
    #     user_repository=repository_container.user_repository,
    #
    #     # Inject Gateways (Infrastructure Services)
    #     generate_otp_service=gateways_container.generate_otp_service,
    #     cache_otp_service=gateways_container.cache_otp_service,
    #     mail_service=gateways_container.mail_service,
    #     password_hasher_service=gateways_container.password_hasher_service
    # )
    #
    # signup_verification_use_case = providers.Factory(
    #     "src.core.domain.usecases.signup_verification.SignupVerificationUseCase",
    #     unit_of_work=repository_container.unit_of_work,
    #     cache_otp_service=gateways_container.cache_otp_service,
    #     token_service=gateways_container.token_service,
    #     cache_token_service=gateways_container.cache_token_service
    # )
    #
    # handle_google_auth_use_case = providers.Factory(
    #     "src.core.domain.usecases.handle_google_auth.HandleGoogleAuthUseCase",
    #     user_repository=repository_container.user_repository,
    #     # token_service=gateways_container.token_service,
    #     # ...
    # )

    # ... User Use Cases ---
    get_user_profile_use_case = providers.Factory(
        GetUserProfileUseCase,
        user_repository=repository_container.user_repository
    )
