import uvicorn
from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from starlette.middleware.cors import CORSMiddleware
from slowapi.errors import RateLimitExceeded

from src.application_container import ApplicationContainer
from src.config.settings import settings
from src.core.common.logger import setup_logging
from src.core.common.exceptions import BusinessException
from src.core.common.constants import MsgKey
from src.core.common.i18n import i18n

from src.presentation.handler import business_exception_handler, validation_exception_handler, create_response, \
    global_exception_handler
from src.presentation.limiter import limiter
from src.presentation.v1.api import api_router
from src.presentation.v1.middleware.auth_middleware import AuthMiddleware
from src.presentation.webhooks import webhook

from .lifespan import lifespan

setup_logging()


def create_app() -> FastAPI:
    container = ApplicationContainer()

    app = FastAPI(
        title=settings.APP_NAME,
        version=settings.APP_VERSION,
        debug=settings.DEBUG,
        lifespan=lifespan
    )

    app.container = container

    app.state.limiter = limiter

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    app.add_middleware(AuthMiddleware)

    app.add_exception_handler(BusinessException, business_exception_handler)
    app.add_exception_handler(RequestValidationError, validation_exception_handler)

    async def custom_rate_limit_handler(request: Request, exc: RateLimitExceeded):
        lang = request.headers.get("accept-language", "vi").split(",")[0].split("-")[0]
        msg = i18n.translate(MsgKey.SPAM_DETECTED, lang)
        return create_response(
            status_code=429,
            message=msg,
            content_data=None
        )

    app.add_exception_handler(RateLimitExceeded, custom_rate_limit_handler)

    app.add_exception_handler(Exception, global_exception_handler)

    app.include_router(api_router, prefix=settings.API_V1_STR)
    app.include_router(webhook.router)

    return app


app = create_app()

if __name__ == "__main__":
    uvicorn.run(
        "src.main.server:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )
