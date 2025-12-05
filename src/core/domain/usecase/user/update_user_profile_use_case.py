from typing import Optional
from fastapi import UploadFile
from loguru import logger

from src.core.common.constants import MsgKey
from src.core.common.exceptions import BusinessException
from src.core.common.util.storage_path import StoragePath

from ..user_credit.ensure_credit_balance_use_case import EnsureCreditBalanceUseCase
from ...dto.user_dto import UserProfileDTO, UserResponse, UserCreditResponse
from ...repository.unit_of_work import UnitOfWork
from ...service.storage_service import StorageService


class UpdateUserProfileUseCase:
    def __init__(
            self,
            unit_of_work: UnitOfWork,
            storage_service: StorageService,
            ensure_balance_use_case: EnsureCreditBalanceUseCase
    ):
        self._uow = unit_of_work
        self._storage_service = storage_service
        self._ensure_balance_use_case = ensure_balance_use_case

    async def execute(
            self,
            user_id: int,
            name: Optional[str] = None,
            avatar_file: Optional[UploadFile] = None
    ) -> UserProfileDTO:
        try:
            async with self._uow as uow:

                logger.info(f"Request body: {user_id} - {name} - {avatar_file}")

                user = await uow.user_repository.get_user_by_id(user_id)
                if not user:
                    raise BusinessException(MsgKey.USER_NOT_FOUND, 404)

                if avatar_file:
                    content_type = avatar_file.content_type

                    if not content_type.startswith("image/"):
                        logger.warning(f"Invalid avatar upload: Type={content_type}")
                        raise BusinessException(MsgKey.AVATAR_FILE_ERROR, 400)

                    new_avatar_url = await self._storage_service.upload_file(
                        file=avatar_file,
                        destination_path=StoragePath.USER_AVATARS
                    )

                    if user.avatar:
                        await self._storage_service.delete_file(user.avatar)

                    user.avatar = new_avatar_url

                if name:
                    clean_name = name.strip()
                    if len(clean_name) < 2:
                        raise BusinessException(MsgKey.VAL_NAME_TOO_SHORT, 400)
                    user.name = clean_name

                updated_user = await uow.user_repository.update_user(user)
                if not updated_user:
                    raise BusinessException(MsgKey.SERVER_ERROR, 500)

                if updated_user.user_credit:
                    updated_credit = await self._ensure_balance_use_case.execute(updated_user, uow_session=uow)
                    updated_user.user_credit = updated_credit

                user_response = UserResponse.model_validate(updated_user)

                if updated_user.user_credit:
                    credit_response = UserCreditResponse.model_validate(updated_user.user_credit)
                else:
                    credit_response = UserCreditResponse(user_id=user.id, balance=0, last_refill_date=None)

                logger.info(f"New DatA: {user_response} - {credit_response}")

                return UserProfileDTO(
                    user=user_response,
                    credit=credit_response
                )

        except BusinessException:
            raise
        except Exception as e:
            logger.exception(f"UpdateUserProfileUseCase error: {e}")
            raise BusinessException(MsgKey.SERVER_ERROR, 500)
