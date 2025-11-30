from datetime import datetime
from typing import Optional

from sqlalchemy import UniqueConstraint, String, DateTime, Enum, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.core.model.user.enums.auth_provider import AuthProvider
from src.core.model.user.enums.user_status import UserStatus
from src.core.model.user.enums.user_tier import UserTier

from ..postgres import Base


class UserEntity(Base):
    __tablename__ = "users"
    __table_args__ = (
        UniqueConstraint("email", name="uq_user_email"),
    )

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100))
    email: Mapped[str] = mapped_column(String(255), unique=True, index=True, nullable=False)
    password: Mapped[Optional[str]] = mapped_column(String(255))
    avatar: Mapped[Optional[str]] = mapped_column(String(500))
    last_login: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True))

    status: Mapped[UserStatus] = mapped_column(
        Enum(UserStatus),
        default=UserStatus.ACTIVE,
        nullable=False
    )

    tier: Mapped[UserTier] = mapped_column(
        Enum(UserTier),
        default=UserTier.FREE,
        nullable=False,
        index=True
    )

    auth_provider: Mapped[AuthProvider] = mapped_column(
        Enum(AuthProvider),
        default=AuthProvider.EMAIL,
        nullable=False
    )

    signin_count: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    sign_out_count: Mapped[int] = mapped_column(Integer, default=0, nullable=False)

    user_credit: Mapped["UserCreditEntity"] = relationship(
        back_populates="user",
        uselist=False,
        cascade="all, delete-orphan"
    )
