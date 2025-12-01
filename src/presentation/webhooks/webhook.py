from fastapi import APIRouter, Depends, Request
from dependency_injector.wiring import inject, Provide
from loguru import logger

from src.application_container import ApplicationContainer
from src.core.domain.usecase.user_credit.verify_ad_mob_reward_use_case import VerifyAdMobRewardUseCase

router = APIRouter(prefix="/webhooks", tags=["AdMob Webhooks"])


@router.get("/admob/reward")
@inject
async def handle_admob_reward_webhook(
        request: Request,
        use_case: VerifyAdMobRewardUseCase = Depends(
            Provide[ApplicationContainer.use_case_package.verify_ad_mob_reward_use_case])
):
    """
    Endpoint nhận Server-Side Verification (SSV) từ Google AdMob.
    Google sẽ gọi GET request kèm theo query params.
    """
    query_params = dict(request.query_params)

    logger.info(f"Received AdMob SSV Webhook: {query_params}")

    await use_case.execute(query_params)
    return {"status": "success"}