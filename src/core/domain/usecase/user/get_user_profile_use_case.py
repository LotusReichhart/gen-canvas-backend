from loguru import logger

from src.core.common.constants import MsgKey
from src.core.common.exceptions import BusinessException

from ...dto.user_dto import UserProfileDTO, UserResponse, UserCreditResponse
from ...repository.unit_of_work import UnitOfWork


class GetUserProfileUseCase:
    def __init__(self,
                 unit_of_work: UnitOfWork):
        self._uow = unit_of_work

    async def execute(self, user_id: int) -> UserProfileDTO:
        try:
            async with self._uow as uow:
                user = await uow.user_repository.get_user_by_id(user_id)

                if not user:
                    raise BusinessException(message_key=MsgKey.USER_NOT_FOUND, status_code=404)

                user_response = UserResponse.model_validate(user)
                credit_response = None
                if user.user_credit:
                    credit_response = UserCreditResponse.model_validate(user.user_credit)

                return UserProfileDTO(user=user_response, credit=credit_response)

        except BusinessException:
            raise

        except Exception as e:
            logger.error(f"GetUserProfileUseCase: {e}")
            raise BusinessException(
                message_key=MsgKey.SERVER_ERROR,
                status_code=500
            )
