from datetime import date
from typing import Optional

from sqlalchemy import ForeignKey, Integer, DateTime, Date, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from ..postgres import Base

class UserCreditEntity(Base):
    __tablename__ = "user_credits"

    id: Mapped[int] = mapped_column(primary_key=True)

    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id"),
        unique=True,
        index=True,
        nullable=False
    )

    balance: Mapped[int] = mapped_column(Integer, default=5, nullable=False)

    last_refill_date: Mapped[date] = mapped_column(
        Date,
        server_default=func.current_date(),
        nullable=False
    )

    last_notification_date: Mapped[Optional[date]] = mapped_column(Date, nullable=True)

    # Quan hệ 1-1: Credit -> User
    user: Mapped["UserEntity"] = relationship(
        back_populates="user_credit"
    )

    # Quan hệ 1-N: Credit -> CreditTransaction
    transactions: Mapped[list["CreditTransactionEntity"]] = relationship(
        back_populates="user_credit",
        cascade="all, delete-orphan"
    )