import re
from src.core.common.constants import MsgKey

EMAIL_REGEX = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"

def is_safe_input(value: str) -> bool:
    return True


def validate_name_logic(name: str) -> str:
    name = name.strip()
    if not name:
        raise ValueError(MsgKey.VAL_NAME_EMPTY.value)
    if len(name) < 2:
        raise ValueError(MsgKey.VAL_NAME_TOO_SHORT.value)
    if not is_safe_input(name):
        raise ValueError(MsgKey.VAL_UNSAFE_INPUT.value)
    return name


def validate_email_logic(email: str) -> str:
    email = email.strip()
    if not email:
        raise ValueError(MsgKey.VAL_EMAIL_EMPTY.value)
    if not re.match(EMAIL_REGEX, email):
        raise ValueError(MsgKey.VAL_EMAIL_INVALID.value)
    if not is_safe_input(email):
        raise ValueError(MsgKey.VAL_UNSAFE_INPUT.value)
    return email


def validate_password_logic(password: str) -> str:
    password = password.strip()
    if not password:
        raise ValueError(MsgKey.VAL_PASSWORD_EMPTY.value)

    if len(password) < 8:
        raise ValueError(MsgKey.VAL_PASSWORD_TOO_SHORT.value)

    if not re.search(r"[A-Z]", password):
        raise ValueError(MsgKey.VAL_PASSWORD_NO_UPPER.value)

    if not re.search(r"[a-z]", password):
        raise ValueError(MsgKey.VAL_PASSWORD_NO_LOWER.value)

    if not re.search(r"[0-9]", password):
        raise ValueError(MsgKey.VAL_PASSWORD_NO_DIGIT.value)

    if not re.search(r"[\W_]", password):
        raise ValueError(MsgKey.VAL_PASSWORD_NO_SPECIAL.value)

    if not is_safe_input(password):
        raise ValueError(MsgKey.VAL_UNSAFE_INPUT.value)

    return password


def validate_otp_logic(otp: str) -> str:
    otp = otp.strip()
    if not otp:
        raise ValueError(MsgKey.VAL_OTP_EMPTY.value)
    if len(otp) != 6 or not otp.isdigit():
        raise ValueError(MsgKey.VAL_OTP_INVALID.value)
    return otp