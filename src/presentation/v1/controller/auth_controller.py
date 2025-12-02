from fastapi import APIRouter, Depends, Request
from dependency_injector.wiring import inject, Provide

from src.application_container import ApplicationContainer
from src.core.common.i18n import i18n
from src.core.common.constants import MsgKey
from src.core.domain.dto.auth_dto import TokenResponse, ResetTokenResponse
from src.core.domain.usecase.auth.password_verification_use_case import PasswordVerificationUseCase
from src.core.domain.usecase.auth.refresh_signin_use_case import RefreshSigninUseCase
from src.core.domain.usecase.auth.request_forgot_password_use_case import RequestForgotPasswordUseCase

from src.core.domain.usecase.auth.request_signup_use_case import RequestSignupUseCase
from src.core.domain.usecase.auth.resend_otp_use_case import ResendOtpUseCase
from src.core.domain.usecase.auth.reset_password_use_case import ResetPasswordUseCase
from src.core.domain.usecase.auth.sign_out_use_case import SignOutUseCase
from src.core.domain.usecase.auth.signin_with_email_use_case import SigninWithEmailUseCase
from src.core.domain.usecase.auth.signin_with_google_use_case import SignInWithGoogleUseCase
from src.core.domain.usecase.auth.signup_verification_use_case import SignupVerificationUseCase

from src.presentation.dependency import get_lang, get_current_user_payload
from ..schema.auth_schema import (
    SignUpRequest,
    VerifySignupRequest,
    SignInRequest,
    RefreshTokenRequest,
    ForgotPasswordRequest,
    GoogleAuthRequest,
    ResendOtpRequest,
    VerifyForgotPasswordRequest,
    ResetPasswordRequest
)
from ..schema.base import BaseResponse
from ...limiter import limiter

router = APIRouter(prefix="/auth", tags=["Authentication"])


@router.post("/signin", response_model=BaseResponse[TokenResponse])
@inject
@limiter.limit("6/minute")
async def signin(
        request: Request,
        body_data: SignInRequest,
        use_case: SigninWithEmailUseCase = Depends(
            Provide[ApplicationContainer.use_case_package.signin_with_email_use_case]),
        lang: str = Depends(get_lang)
):
    result = await use_case.execute(email=body_data.email, password=body_data.password)
    return BaseResponse(
        status=200,
        message=i18n.translate(MsgKey.LOGIN_SUCCESS, lang),
        data=result
    )


@router.post("/signup", response_model=BaseResponse)
@inject
@limiter.limit("6/minute")
async def request_signup(
        request: Request,
        body_data: SignUpRequest,
        use_case: RequestSignupUseCase = Depends(
            Provide[ApplicationContainer.use_case_package.request_signup_use_case]),
        lang: str = Depends(get_lang)
):
    await use_case.execute(email=body_data.email, name=body_data.name, password=body_data.password)
    return BaseResponse(
        status=200,
        message=i18n.translate(MsgKey.OTP_SENT, lang)
    )


@router.post("/signup/verify", response_model=BaseResponse[TokenResponse])
@inject
@limiter.limit("6/minute")
async def verify_signup(
        request: Request,
        body_data: VerifySignupRequest,
        use_case: SignupVerificationUseCase = Depends(
            Provide[ApplicationContainer.use_case_package.signup_verification_use_case]),
        lang: str = Depends(get_lang)
):
    result = await use_case.execute(email=body_data.email, otp=body_data.otp)
    return BaseResponse(
        status=200,
        message=i18n.translate(MsgKey.USER_CREATED, lang),
        data=result
    )


@router.post("/refresh", response_model=BaseResponse[TokenResponse])
@inject
@limiter.limit("6/minute")
async def refresh_signin(
        request: Request,
        body_data: RefreshTokenRequest,
        use_case: RefreshSigninUseCase = Depends(
            Provide[ApplicationContainer.use_case_package.refresh_signin_use_case]),
        lang: str = Depends(get_lang)
):
    result = await use_case.execute(refresh_token=body_data.refresh_token)
    return BaseResponse(
        status=200,
        message=i18n.translate(MsgKey.SUCCESS, lang),
        data=result
    )


@router.post("/sign-out", response_model=BaseResponse)
@inject
async def sign_out(
        user_payload: dict = Depends(get_current_user_payload),
        use_case: SignOutUseCase = Depends(Provide[ApplicationContainer.use_case_package.sign_out_use_case]),
        lang: str = Depends(get_lang)
):
    await use_case.execute(
        user_id=user_payload.get("id"),
        signin_count=user_payload.get("signin_count"),
        sign_out_count=user_payload.get("sign_out_count")
    )
    return BaseResponse(
        status=200,
        message=i18n.translate(MsgKey.SUCCESS, lang)
    )


@router.post("/password/forgot", response_model=BaseResponse)
@inject
@limiter.limit("6/minute")
async def request_forgot_password(
        request: Request,
        body_data: ForgotPasswordRequest,
        use_case: RequestForgotPasswordUseCase = Depends(
            Provide[ApplicationContainer.use_case_package.request_forgot_password_use_case]),
        lang: str = Depends(get_lang)
):
    await use_case.execute(email=body_data.email)

    return BaseResponse(
        status=200,
        message=i18n.translate(MsgKey.OTP_SENT, lang)
    )


@router.post("/google", response_model=BaseResponse[TokenResponse])
@inject
@limiter.limit("6/minute")
async def google_auth(
        request: Request,
        body_data: GoogleAuthRequest,
        use_case: SignInWithGoogleUseCase = Depends(
            Provide[ApplicationContainer.use_case_package.signin_with_google_use_case]),
        lang: str = Depends(get_lang)
):
    result = await use_case.execute(user_id_token=body_data.user_id_token)

    return BaseResponse(
        status=200,
        message=i18n.translate(MsgKey.LOGIN_SUCCESS, lang),
        data=result
    )


# --- 4. OTP RESEND ---
@router.post("/otp/resend", response_model=BaseResponse)
@inject
@limiter.limit("6/minute")
async def resend_otp(
        request: Request,
        body_data: ResendOtpRequest,
        use_case: ResendOtpUseCase = Depends(Provide[ApplicationContainer.use_case_package.resend_otp_use_case]),
        lang: str = Depends(get_lang)
):
    await use_case.execute(email=body_data.email)

    return BaseResponse(
        status=200,
        message=i18n.translate(MsgKey.OTP_SENT, lang)
    )


@router.post("/password/verify", response_model=BaseResponse[ResetTokenResponse])
@inject
@limiter.limit("6/minute")
async def verify_forgot_password(
        request: Request,
        body_data: VerifyForgotPasswordRequest,
        use_case: PasswordVerificationUseCase = Depends(
            Provide[ApplicationContainer.use_case_package.password_verification_use_case]),
        lang: str = Depends(get_lang)
):
    result = await use_case.execute(email=body_data.email, otp=body_data.otp)

    return BaseResponse(
        status=200,
        message=i18n.translate(MsgKey.VERIFY_SUCCESS, lang),
        data=result
    )


@router.post("/password/reset", response_model=BaseResponse)
@inject
@limiter.limit("6/minute")
async def reset_password(
        request: Request,
        body_data: ResetPasswordRequest,
        use_case: ResetPasswordUseCase = Depends(
            Provide[ApplicationContainer.use_case_package.reset_password_use_case]),
        lang: str = Depends(get_lang)
):
    await use_case.execute(
        reset_token=body_data.reset_token,
        new_password=body_data.new_password
    )

    return BaseResponse(
        status=200,
        message=i18n.translate(MsgKey.PASSWORD_CHANGED, lang)
    )
