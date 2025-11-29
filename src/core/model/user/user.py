from dataclasses import field
from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict

from .enums.auth_provider import AuthProvider
from .enums.user_status import UserStatus
from .enums.user_tier import UserTier

from .user_credit import UserCredit

class User(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: Optional[int] = None
    name: str
    email: str
    password: Optional[str] = None
    avatar: Optional[str] = None
    last_login: datetime | None
    signin_count: int = field(default=0)
    sign_out_count: int = field(default=0)
    status: UserStatus = UserStatus.ACTIVE

    tier: UserTier = UserTier.FREE
    auth_provider: AuthProvider = AuthProvider.EMAIL

    user_credit: Optional[UserCredit] = None

    def increase_signin_count(self):
        self.signin_count += 1

    def increase_sign_out_count(self):
        self.sign_out_count += 1