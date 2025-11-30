from enum import Enum


class MsgKey(str, Enum):
    # Success
    SUCCESS = "success"
    USER_CREATED = "user_created"
    LOGIN_SUCCESS = "login_success"

    # Errors (Business)
    SPAM_DETECTED = "spam_detected"
    AUTH_REQUIRED = "auth_required"
    FORBIDDEN = "forbidden"
    EMAIL_EXISTS = "email_exists"

    GOOGLE_AUTH_FAILED = "google_auth_failed"
    INVALID_TOKEN = "invalid_token"

    EMAIL_NOT_FOUND = "email_not_found"
    WRONG_PASSWORD = "wrong_password"

    INVALID_OTP = "invalid_otp"

    USER_NOT_FOUND = "user_not_found"
    USER_CREDIT_NOT_FOUND = "user_credit_not_found"

    # Errors (Validation generic)
    VALIDATION_ERROR = "validation_error"
    SERVER_ERROR = "server_error"
