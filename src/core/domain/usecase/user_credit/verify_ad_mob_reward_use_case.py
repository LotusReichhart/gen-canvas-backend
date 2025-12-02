from loguru import logger
from datetime import datetime, timezone
from typing import Any

from src.core.common.constants import MsgKey
from src.core.common.exceptions import BusinessException
from src.core.model.user.credit_transaction import CreditTransaction
from src.core.model.user.enums.credit_transaction_source import CreditTransactionSource

from ...repository.unit_of_work import UnitOfWork
from ...service.ad_mob_verification_service import AdMobVerificationService


class VerifyAdMobRewardUseCase:
    """
    Use Case này xử lý Webhook SSV từ Google AdMob.
    Nó xác thực và cộng thưởng cho user.
    """

    def __init__(self,
                 unit_of_work: UnitOfWork,
                 admob_verification_service: AdMobVerificationService):
        self.uow = unit_of_work
        self.admob_verification_service = admob_verification_service

    async def execute(self, query_params: dict[str, Any]):
        try:
            reward_amount = 1

            is_valid = await self.admob_verification_service.verify_reward_webhook(query_params)

            logger.info(f"AdMob SSV is_valid: ${is_valid}")

            if not is_valid:
                raise BusinessException(
                    message_key=MsgKey.FORBIDDEN,
                    status_code=403
                )

            user_id_str = query_params.get("user_id")
            if not user_id_str:
                logger.info("AdMob SSV: Received a valid verification 'ping' (no user_id).")
                return

            user_id = int(user_id_str)

            async with self.uow as uow:
                user_credit = await uow.credit_repository.get_user_credit_by_user_id(user_id)
                if not user_credit:
                    raise BusinessException(
                        message_key=MsgKey.USER_CREDIT_NOT_FOUND,
                        status_code=404
                    )

                user_credit.balance += reward_amount
                await uow.credit_repository.update_user_credit(user_credit)

                transaction = CreditTransaction(
                    credit_id=user_credit.id,
                    amount=reward_amount,
                    source=CreditTransactionSource.AD_REWARD,
                    created_at=datetime.now(timezone.utc),
                    balance_after=user_credit.balance
                )
                await uow.credit_transaction_repository.create_transaction(transaction)

            logger.info(f"Successfully rewarded user {user_id} from AdMob webhook.")

        except BusinessException as e:
            logger.error(f"VerifyAdMobRewardUseCase AppError: {e}")
            raise
        except Exception as e:
            logger.error(f"VerifyAdMobRewardUseCase Exception: {e}")
            raise BusinessException(
                message_key=MsgKey.SERVER_ERROR,
                status_code=500
            )
