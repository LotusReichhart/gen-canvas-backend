from datetime import date
from typing import Optional

from pydantic import BaseModel

from src.core.model.user.enums.auth_provider import AuthProvider
from src.core.model.user.enums.user_status import UserStatus
from src.core.model.user.enums.user_tier import UserTier


class UserResponse(BaseModel):
    id: int
    username: str
    email: str
    avatar: Optional[str] = None
    status: UserStatus = UserStatus.ACTIVE
    tier: UserTier = UserTier.FREE
    auth_provider: AuthProvider = AuthProvider.EMAIL

    class Config:
        from_attributes = True


class UserCreditResponse(BaseModel):
    balance: int
    last_refill_processed_date: Optional[date] = None

    class Config:
        from_attributes = True


class UserProfileDTO(BaseModel):
    user: UserResponse
    credit: Optional[UserCreditResponse] = None