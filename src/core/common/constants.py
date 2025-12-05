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

    FILE_TOO_LARGE = "file_too_large"
    FILE_EMPTY = "file_empty"
    UPLOAD_FAILED = "upload_failed"

    OTP_SENT = "otp_sent"
    VERIFY_SUCCESS = "verify_success"
    PASSWORD_CHANGED = "password_changed"

    VAL_NAME_EMPTY = "val_name_empty"
    VAL_NAME_TOO_SHORT = "val_name_too_short"
    VAL_EMAIL_EMPTY = "val_email_empty"
    VAL_EMAIL_INVALID = "val_email_invalid"
    VAL_PASSWORD_EMPTY = "val_password_empty"
    VAL_PASSWORD_TOO_SHORT = "val_password_too_short"
    VAL_PASSWORD_NO_UPPER = "val_password_no_upper"
    VAL_PASSWORD_NO_LOWER = "val_password_no_lower"
    VAL_PASSWORD_NO_DIGIT = "val_password_no_digit"
    VAL_PASSWORD_NO_SPECIAL = "val_password_no_special"
    VAL_OTP_EMPTY = "val_otp_empty"
    VAL_OTP_INVALID = "val_otp_invalid"
    VAL_UNSAFE_INPUT = "val_unsafe_input"
    VAL_CONFIRM_PASSWORD_EMPTY = "val_confirm_password_empty"
    VAL_PASSWORD_MISMATCH = "val_password_mismatch"

    UPDATE_SUCCESS = "update_success"
    AVATAR_FILE_ERROR = "avatar_file_error"

    # Errors (Validation generic)
    VALIDATION_ERROR = "validation_error"
    SERVER_ERROR = "server_error"
