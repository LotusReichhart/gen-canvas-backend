from enum import Enum


class MsgKey(str, Enum):
    # Success
    SUCCESS = "success"
    USER_CREATED = "user_created"

    # Errors (Business)
    SPAM_DETECTED = "spam_detected"
    AUTH_REQUIRED = "auth_required"
    EMAIL_EXISTS = "email_exists"
    USER_NOT_FOUND = "user_not_found"

    # Errors (Validation generic)
    VALIDATION_ERROR = "validation_error"
    SERVER_ERROR = "server_error"