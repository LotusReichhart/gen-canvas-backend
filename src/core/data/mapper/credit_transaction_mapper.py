from src.core.model.user.credit_transaction import CreditTransaction

from ..database.model.credit_transaction_entity import CreditTransactionEntity


class CreditTransactionMapper:
    @staticmethod
    def to_model(entity: CreditTransactionEntity) -> CreditTransaction:
        return CreditTransactionEntity(
            id=entity.id,
            credit_id=entity.credit_id,
            amount=entity.amount,
            source=entity.source,
            balance_after=entity.balance_after,
            created_at=entity.created_at
        )

    @staticmethod
    def to_entity(credit_transaction: CreditTransaction) -> CreditTransactionEntity:
        return CreditTransactionEntity(
            credit_id=credit_transaction.credit_id,
            amount=credit_transaction.amount,
            source=credit_transaction.source,
            balance_after=credit_transaction.balance_after
        )
