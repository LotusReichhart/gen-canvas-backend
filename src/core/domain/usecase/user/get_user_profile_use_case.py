from loguru import logger

from src.core.common.constants import MsgKey
from src.core.common.exceptions import BusinessException

from ..user_credit.ensure_credit_balance_use_case import EnsureCreditBalanceUseCase
from ...dto.user_dto import UserProfileDTO, UserResponse, UserCreditResponse
from ...repository.unit_of_work import UnitOfWork


class GetUserProfileUseCase:
    def __init__(self,
                 unit_of_work: UnitOfWork,
                 ensure_balance_use_case: EnsureCreditBalanceUseCase):
        self._uow = unit_of_work
        self._ensure_balance_use_case = ensure_balance_use_case

    async def execute(self, user_id: int) -> UserProfileDTO:
        try:
            async with self._uow as uow:
                user = await uow.user_repository.get_user_by_id(user_id)

                if not user:
                    raise BusinessException(message_key=MsgKey.USER_NOT_FOUND, status_code=404)

                if user.user_credit:
                    updated_credit = await self._ensure_balance_use_case.execute(user, uow_session=uow)
                    user.user_credit = updated_credit

                user_response = UserResponse.model_validate(user)

                if user.user_credit:
                    credit_response = UserCreditResponse.model_validate(user.user_credit)
                else:
                    credit_response = UserCreditResponse(user_id=user.id, balance=0, last_refill_date=None)

                return UserProfileDTO(user=user_response, credit=credit_response)

        except BusinessException:
            raise

        except Exception as e:
            logger.error(f"GetUserProfileUseCase: {e}")
            raise BusinessException(
                message_key=MsgKey.SERVER_ERROR,
                status_code=500
            )
