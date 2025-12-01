from typing import Annotated

from pydantic import BaseModel, Field, model_validator, AfterValidator

from src.core.common.util.validators import (
    validate_name_logic,
    validate_email_logic,
    validate_password_logic,
    validate_otp_logic
)

NameField = Annotated[str, AfterValidator(validate_name_logic)]
EmailField = Annotated[str, AfterValidator(validate_email_logic)]
PasswordField = Annotated[str, AfterValidator(validate_password_logic)]
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
    password: str

    @model_validator(mode='after')
    def check_empty(self) -> 'SignInRequest':
        from src.core.common.constants import MsgKey
        if not self.password:
            raise ValueError(MsgKey.VAL_PASSWORD_EMPTY)
        return self


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
    confirm_password: str

    @model_validator(mode='after')
    def check_passwords_match(self) -> 'ResetPasswordRequest':
        if self.new_password != self.confirm_password:
            raise ValueError('Mật khẩu xác nhận không khớp')
        return self


# --- RESEND OTP ---
class ResendOtpRequest(BaseModel):
    email: EmailField
