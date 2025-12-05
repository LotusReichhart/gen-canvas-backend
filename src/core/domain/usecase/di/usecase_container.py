from dependency_injector import containers, providers

from ..auth.password_verification_use_case import PasswordVerificationUseCase
from ..auth.refresh_signin_use_case import RefreshSigninUseCase
from ..auth.request_forgot_password_use_case import RequestForgotPasswordUseCase
from ..auth.request_signup_use_case import RequestSignupUseCase
from ..auth.resend_otp_use_case import ResendOtpUseCase
from ..auth.reset_password_use_case import ResetPasswordUseCase
from ..auth.sign_out_use_case import SignOutUseCase
from ..auth.signin_with_email_use_case import SigninWithEmailUseCase
from ..auth.signin_with_google_use_case import SignInWithGoogleUseCase
from ..auth.signup_verification_use_case import SignupVerificationUseCase
from ..banner.get_list_banner_use_case import GetListBannerUseCase
from ..user.get_user_profile_use_case import GetUserProfileUseCase
from ..user.update_user_profile_use_case import UpdateUserProfileUseCase
from ..user_credit.ensure_credit_balance_use_case import EnsureCreditBalanceUseCase
from ..user_credit.verify_ad_mob_reward_use_case import VerifyAdMobRewardUseCase


class UseCaseContainer(containers.DeclarativeContainer):
    config = providers.Configuration()
    repository_container = providers.DependenciesContainer()
    service_container = providers.DependenciesContainer()

    ensure_credit_balance_use_case = providers.Factory(
        EnsureCreditBalanceUseCase,
        unit_of_work=repository_container.unit_of_work,
        user_calculator_service=service_container.user_credit_calculator_service
    )

    # --- Auth Use Cases ---

    # --- Signin ---
    signin_with_email_use_case: SigninWithEmailUseCase = providers.Factory(
        SigninWithEmailUseCase,
        unit_of_work=repository_container.unit_of_work,
        password_hasher_service=service_container.password_hasher_service,
        token_service=service_container.token_service,
        cache_token_service=service_container.cache_token_service,
    )

    signin_with_google_use_case: SignInWithGoogleUseCase = providers.Factory(
        SignInWithGoogleUseCase,
        unit_of_work=repository_container.unit_of_work,
        token_service=service_container.token_service,
        cache_token_service=service_container.cache_token_service,
        client_id=config.GOOGLE_CLIENT_ID
    )

    # --- Signup ---
    request_signup_use_case: RequestSignupUseCase = providers.Factory(
        RequestSignupUseCase,
        unit_of_work=repository_container.unit_of_work,
        generate_otp_service=service_container.generate_otp_service,
        cache_otp_service=service_container.cache_otp_service,
        mail_service=service_container.mail_service,
        password_hasher_service=service_container.password_hasher_service
    )

    signup_verification_use_case: SignupVerificationUseCase = providers.Factory(
        SignupVerificationUseCase,
        unit_of_work=repository_container.unit_of_work,
        cache_otp_service=service_container.cache_otp_service,
        token_service=service_container.token_service,
        cache_token_service=service_container.cache_token_service
    )

    # --- Forgot password ---
    request_forgot_password_use_case: RequestForgotPasswordUseCase = providers.Factory(
        RequestForgotPasswordUseCase,
        unit_of_work=repository_container.unit_of_work,
        generate_otp_service=service_container.generate_otp_service,
        cache_otp_service=service_container.cache_otp_service,
        mail_service=service_container.mail_service
    )

    password_verification_use_case: PasswordVerificationUseCase = providers.Factory(
        PasswordVerificationUseCase,
        token_service=service_container.token_service,
        cache_otp_service=service_container.cache_otp_service,
        cache_token_service=service_container.cache_token_service,
    )

    reset_password_use_case: ResetPasswordUseCase = providers.Factory(
        ResetPasswordUseCase,
        unit_of_work=repository_container.unit_of_work,
        cache_token_service=service_container.cache_token_service,
        password_hasher_service=service_container.password_hasher_service
    )

    # --- Resend OTP ---
    resend_otp_use_case: ResendOtpUseCase = providers.Factory(
        ResendOtpUseCase,
        generate_otp_service=service_container.generate_otp_service,
        cache_otp_service=service_container.cache_otp_service,
        mail_service=service_container.mail_service
    )

    # --- Sign Out ---
    sign_out_use_case: SignOutUseCase = providers.Factory(
        SignOutUseCase,
        unit_of_work=repository_container.unit_of_work,
        cache_token_service=service_container.cache_token_service,
    )

    # --- Refresh
    refresh_signin_use_case: RefreshSigninUseCase = providers.Factory(
        RefreshSigninUseCase,
        unit_of_work=repository_container.unit_of_work,
        token_service=service_container.token_service,
        cache_token_service=service_container.cache_token_service
    )

    # --- User ---
    get_user_profile_use_case: GetUserProfileUseCase = providers.Factory(
        GetUserProfileUseCase,
        unit_of_work=repository_container.unit_of_work,
        ensure_balance_use_case=ensure_credit_balance_use_case
    )

    update_user_profile_use_case = providers.Factory(
        UpdateUserProfileUseCase,
        unit_of_work=repository_container.unit_of_work,
        storage_service=service_container.storage_service,
        ensure_balance_use_case=ensure_credit_balance_use_case
    )

    # --- User Credit ---
    verify_ad_mob_reward_use_case: VerifyAdMobRewardUseCase = providers.Factory(
        VerifyAdMobRewardUseCase,
        unit_of_work=repository_container.unit_of_work,
        admob_verification_service=service_container.admob_verification_service
    )

    # --- Banner ---
    get_list_banner_use_case: GetListBannerUseCase = providers.Factory(
        GetListBannerUseCase,
        unit_of_work=repository_container.unit_of_work,
    )
