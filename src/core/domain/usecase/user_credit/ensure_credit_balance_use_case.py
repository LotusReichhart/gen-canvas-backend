from datetime import datetime, timezone
from loguru import logger

from src.core.model.user.user import User
from src.core.model.user.enums.credit_transaction_source import CreditTransactionSource
from src.core.model.user.credit_transaction import CreditTransaction
from src.core.model.user.user_credit import UserCredit

from ...repository.unit_of_work import UnitOfWork
from ...service.user_credit_calculator_service import UserCreditCalculatorService


class EnsureCreditBalanceUseCase:
    def __init__(
            self,
            unit_of_work: UnitOfWork,
            user_calculator_service: UserCreditCalculatorService
    ):
        self._uow = unit_of_work
        self._calculator = user_calculator_service

    async def execute(self, user: User, uow_session=None) -> UserCredit:
        if not user.user_credit:
            return UserCredit(user_id=user.id, balance=0, last_refill_date=None)

        result = self._calculator.calculate_refill(
            current_balance=user.user_credit.balance,
            last_refill_date=user.user_credit.last_refill_date,
            tier=user.tier
        )

        if not result["should_update"]:
            return user.user_credit

        user.user_credit.balance = result["new_balance"]
        user.user_credit.last_refill_date = result["refill_date"]

        repo = self._uow.user_credit_repository if uow_session else self._uow.user_credit_repository

        await repo.update_user_credit(user.user_credit)

        refill_amount = result["refill_amount"]
        if refill_amount > 0:
            transaction = CreditTransaction(
                id=0,
                credit_id=user.user_credit.id,
                amount=refill_amount,
                source=CreditTransactionSource.DAILY_REFILL,
                balance_after=result["new_balance"],
                created_at=datetime.now(timezone.utc)
            )
            await self._uow.credit_transaction_repository.create_transaction(transaction)
            logger.info(f"Lazy Refill: User {user.id} +{refill_amount} credits")

        return user.user_credit
