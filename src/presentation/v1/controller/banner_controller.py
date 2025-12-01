from typing import List
from fastapi import APIRouter, Depends, Request
from dependency_injector.wiring import inject, Provide

from src.application_container import ApplicationContainer

from src.core.common.i18n import i18n
from src.core.common.constants import MsgKey
from src.core.domain.dto.banner_dto import BannerResponse
from src.core.domain.usecase.banner.get_list_banner_use_case import GetListBannerUseCase

from ...dependency import get_lang
from ...limiter import limiter
from ..schema.base import BaseResponse

router = APIRouter(prefix="/banners", tags=["Banners"])

@router.get("/", response_model=BaseResponse[List[BannerResponse]])
@inject
@limiter.limit("15/minute")
async def get_all_banners(
    request: Request,
    use_case: GetListBannerUseCase = Depends(Provide[ApplicationContainer.use_case_package.get_list_banner_use_case]),
    lang: str = Depends(get_lang)
):
    """
    Lấy danh sách các banner đang hoạt động (Is Active).
    """

    banners_dto = await use_case.execute()

    return BaseResponse(
        status=200,
        message=i18n.translate(MsgKey.SUCCESS, lang),
        data=banners_dto
    )