from fastapi import Request, status
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from loguru import logger

from src.core.common.exceptions import BusinessException
from src.core.common.i18n import i18n
from src.core.common.constants import MsgKey

from src.presentation.dependency import get_lang


def create_response(status_code: int, message: str, content_data: dict = None):
    return JSONResponse(
        status_code=status_code,
        content={
            "status": status_code,
            "message": message,
            "data": content_data
        }
    )


async def business_exception_handler(request: Request, exc: BusinessException):
    lang = get_lang(request.headers.get("accept-language", "vi"))

    if exc.error_details:
        trans_errors = {}
        for field, key in exc.error_details.items():
            trans_errors[field] = i18n.translate(key, lang)

        msg = i18n.translate(exc.message_key, lang)
        return create_response(
            status_code=exc.status_code,
            message=msg,
            content_data={"error": trans_errors}
        )
    else:
        msg = i18n.translate(exc.message_key, lang)
        return create_response(
            status_code=exc.status_code,
            message=msg,
            content_data=None
        )


async def validation_exception_handler(request: Request, exc: RequestValidationError):
    lang = get_lang(request.headers.get("accept-language", "vi"))
    errors = {}

    for err in exc.errors():
        field = err["loc"][-1] if err["loc"] else "unknown"
        msg_content = err["msg"]

        if "Value error," in msg_content:
            try:
                error_key = msg_content.split("Value error, ")[1].strip()
                translated_msg = i18n.translate(error_key, lang)

                if translated_msg == error_key:
                    pass
                errors[field] = translated_msg
            except IndexError:
                errors[field] = msg_content
        else:
            if err["type"] == "missing":
                errors[field] = i18n.translate(MsgKey.VALIDATION_ERROR, lang)
            else:
                errors[field] = msg_content

    general_msg = i18n.translate(MsgKey.VALIDATION_ERROR, lang)
    return create_response(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        message= general_msg,
        content_data={"error": errors}
    )


async def global_exception_handler(request: Request, exc: Exception):
    lang = get_lang(request.headers.get("accept-language", "vi"))
    msg = i18n.translate(MsgKey.SERVER_ERROR, lang)

    logger.error(f"Unhandled Exception: {exc}")

    return create_response(
        status_code=500,
        message=msg,
        content_data=None
    )
