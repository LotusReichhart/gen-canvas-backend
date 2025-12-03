from typing import Annotated

from pydantic import BaseModel, Field, AfterValidator, field_validator, ValidationInfo

from src.core.common.constants import MsgKey
from src.core.common.util.validators import (
    validate_name_logic,
    validate_email_logic,
    validate_password_logic,
    validate_otp_logic,
    validate_confirm_password_logic
)

NameField = Annotated[str, AfterValidator(validate_name_logic)]
EmailField = Annotated[str, AfterValidator(validate_email_logic)]
PasswordField = Annotated[str, AfterValidator(validate_password_logic)]
ConfirmPasswordField = Annotated[str, AfterValidator(validate_confirm_password_logic)]
OtpField = Annotated[str, AfterValidator(validate_otp_logic)]


# --- SIGN UP ---
class SignUpRequest(BaseModel):
    name: NameField
    email: EmailField
    password: PasswordField


class VerifySignupRequest(BaseModel):
    email: EmailField
    otp: OtpField


# --- SIGN IN ---
class SignInRequest(BaseModel):
    email: EmailField
    password: PasswordField


class RefreshTokenRequest(BaseModel):
    refresh_token: str


class GoogleAuthRequest(BaseModel):
    user_id_token: str = Field(..., min_length=1, description="Google ID Token")


# --- FORGOT PASSWORD ---
class ForgotPasswordRequest(BaseModel):
    email: EmailField


class VerifyForgotPasswordRequest(BaseModel):
    email: EmailField
    otp: OtpField


class ResetPasswordRequest(BaseModel):
    reset_token: str
    new_password: PasswordField
    confirm_password: ConfirmPasswordField

    @field_validator('confirm_password')
    @classmethod
    def check_passwords_match(cls, v: str, info: ValidationInfo) -> str:
        if 'new_password' in info.data:
            if v != info.data['new_password']:
                raise ValueError(MsgKey.VAL_PASSWORD_MISMATCH.value)
        return v


# --- RESEND OTP ---
class ResendOtpRequest(BaseModel):
    email: EmailField
