from fastapi import APIRouter, Depends, Request
from dependency_injector.wiring import inject, Provide

from src.config.settings import settings
from src.core.common.i18n import i18n
from src.core.common.constants import MsgKey
from ...dependency import get_lang

from ...limiter import limiter
from ..schema.base import BaseResponse

router = APIRouter(prefix="/legal", tags=["Legal Info"])


@router.get("/info")
@limiter.limit("5/minute")
async def get_legal_info(
        request: Request,
        lang: str = Depends(get_lang)
):
    """
    Lấy thông tin phiên bản và link của Điều khoản sử dụng & Chính sách bảo mật.
    """
    data = {
        "terms_of_service": {
            "version": settings.TERMS_OF_SERVICE_VERSION,
            "url": f"{settings.TERMS_URL}/{lang}",
        },
        "privacy_policy": {
            "version": settings.PRIVACY_POLICY_VERSION,
            "url": f"{settings.PRIVACY_URL}/{lang}",
        }
    }
    return BaseResponse(
        status=200,
        message=i18n.translate(MsgKey.SUCCESS, lang),
        data=data
    )
