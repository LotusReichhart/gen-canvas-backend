from fastapi import APIRouter, Depends, Request
from dependency_injector.wiring import inject, Provide

from src.application_container import ApplicationContainer

from src.core.common.constants import MsgKey
from src.core.common.i18n import i18n
from src.core.domain.dto.user_dto import UserProfileDTO
from src.core.domain.usecase.user.get_user_profile_use_case import GetUserProfileUseCase

from ...dependency import get_current_user_id, get_lang
from ...limiter import limiter
from ..schema.base import BaseResponse

router = APIRouter(prefix="/users", tags=["Users"])


@router.get("/me", response_model=BaseResponse[UserProfileDTO])
@inject
@limiter.limit("15/minute")
async def get_user_profile(
        request: Request,
        user_id: int = Depends(get_current_user_id),
        use_case: GetUserProfileUseCase = Depends(
            Provide[ApplicationContainer.use_case_package.get_user_profile_use_case]),
        lang: str = Depends(get_lang)
):
    """
    Lấy thông tin profile của người dùng hiện tại.
    Yêu cầu: Access Token hợp lệ (đã được AuthMiddleware xử lý).
    """
    profile_dto = await use_case.execute(user_id)

    return BaseResponse(
        status=200,
        message=i18n.translate(MsgKey.SUCCESS, lang),
        data=profile_dto
    )
