import jwt
from fastapi import Request, status
from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint
from starlette.responses import Response
from loguru import logger

from src.config.settings import settings
from src.core.common.constants import MsgKey
from src.core.common.i18n import i18n

from ...handler import create_response


class AuthMiddleware(BaseHTTPMiddleware):
    def __init__(self, app):
        super().__init__(app)
        self.public_paths = [
            f"{settings.API_V1_STR}/auth/signin",
            f"{settings.API_V1_STR}/auth/signup",
            f"{settings.API_V1_STR}/auth/otp",
            f"{settings.API_V1_STR}/auth/refresh",
            f"{settings.API_V1_STR}/auth/google",
            f"{settings.API_V1_STR}/auth/password",
            f"{settings.API_V1_STR}/banners",
            f"{settings.API_V1_STR}/legal",
            "/webhooks",
            "/favicon.ico"
        ]

    async def dispatch(self, request: Request, call_next: RequestResponseEndpoint) -> Response:
        lang = request.headers.get("accept-language", "vi").split(",")[0].split("-")[0]

        def error_res(status_code: int, key: str):
            msg = i18n.translate(key, lang)
            return create_response(status_code=status_code, message=msg, content_data=None)

        try:
            if any(request.url.path.startswith(path) for path in self.public_paths):
                return await call_next(request)

            if request.method == "OPTIONS":
                return await call_next(request)

            auth_header = request.headers.get("Authorization")
            if not auth_header:
                return error_res(status.HTTP_401_UNAUTHORIZED, MsgKey.AUTH_REQUIRED)

            try:
                scheme, token = auth_header.split()
                if scheme.lower() != "bearer":
                    return error_res(status.HTTP_401_UNAUTHORIZED, MsgKey.INVALID_TOKEN)
            except ValueError:
                return error_res(status.HTTP_401_UNAUTHORIZED, MsgKey.INVALID_TOKEN)

            try:
                payload = jwt.decode(
                    token,
                    key=settings.JWT_ACCESS_SECRET,
                    algorithms=["HS256"]
                )
            except jwt.ExpiredSignatureError:
                return error_res(status.HTTP_401_UNAUTHORIZED, MsgKey.AUTH_REQUIRED)
            except jwt.InvalidTokenError as e:
                logger.warning(f"Invalid Token attempt: {e}")
                return error_res(status.HTTP_401_UNAUTHORIZED, MsgKey.INVALID_TOKEN)

            request.state.user = {
                "id": payload.get("id"),
                "signin_count": payload.get("signin_count"),
                "sign_out_count": payload.get("sign_out_count"),
                "refresh_jti": payload.get("refresh_jti"),
            }

            return await call_next(request)

        except Exception as e:
            logger.error(f"Unhandled error in AuthMiddleware: {e}")
            return error_res(status.HTTP_500_INTERNAL_SERVER_ERROR, MsgKey.SERVER_ERROR)
