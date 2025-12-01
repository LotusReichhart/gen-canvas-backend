from datetime import date
from typing import Optional

from sqlalchemy import ForeignKey, Integer, DateTime
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

    last_refill_processed_date: Mapped[Optional[date]] = mapped_column(DateTime(timezone=True))

    # Quan hệ 1-1: Credit -> User
    user: Mapped["UserEntity"] = relationship(
        back_populates="user_credit"
    )

    # Quan hệ 1-N: Credit -> CreditTransaction
    transactions: Mapped[list["CreditTransactionEntity"]] = relationship(
        back_populates="user_credit",
        cascade="all, delete-orphan"
    )