from src.core.model.user.user_credit import UserCredit

from ..database.model.user_credit_entity import UserCreditEntity


class UserCreditMapper:
    @staticmethod
    def to_model(user_credit_entity: UserCreditEntity) -> UserCredit:
        return UserCredit(
            id=user_credit_entity.id,
            user_id=user_credit_entity.user_id,
            balance=user_credit_entity.balance,
            last_refill_processed_date=user_credit_entity.last_refill_processed_date
        )

    @staticmethod
    def to_entity(user_credit: UserCredit) -> UserCreditEntity:
        return UserCreditEntity(
            user_id=user_credit.user_id,
            balance=user_credit.balance,
            last_refill_processed_date=user_credit.last_refill_processed_date
        )

    @staticmethod
    def to_update_entity(entity: UserCreditEntity, user_credit: UserCredit) -> None:
        entity.balance = user_credit.balance
        entity.last_refill_processed_date = user_credit.last_refill_processed_date
