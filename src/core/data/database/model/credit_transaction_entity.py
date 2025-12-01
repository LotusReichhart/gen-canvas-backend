from datetime import datetime

from sqlalchemy import ForeignKey, Integer, Enum, DateTime, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.core.model.user.enums.credit_transaction_source import CreditTransactionSource
from ..postgres import Base

class CreditTransactionEntity(Base):
    __tablename__ = "credit_transactions"

    id: Mapped[int] = mapped_column(primary_key=True)

    credit_id: Mapped[int] = mapped_column(
        ForeignKey("user_credits.id"),
        index=True,
        nullable=False
    )

    amount: Mapped[int] = mapped_column(Integer, nullable=False)

    source: Mapped[CreditTransactionSource] = mapped_column(
        Enum(CreditTransactionSource),
        nullable=False,
        index=True
    )

    balance_after: Mapped[int] = mapped_column(Integer, nullable=False)

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False
    )

    # Quan hệ N-1: CreditTransaction -> Credit
    user_credit: Mapped["UserCreditEntity"] = relationship(
        back_populates="transactions"
    )