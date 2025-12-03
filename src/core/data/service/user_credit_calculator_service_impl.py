from datetime import date
from typing import Dict, Any

from src.core.domain.service.user_credit_calculator_service import UserCreditCalculatorService
from src.core.model.user.user import UserTier
from src.core.model.user.user_credit_policy import UserCreditPolicy


class UserCreditCalculatorServiceImpl(UserCreditCalculatorService):
    def calculate_refill(
            self,
            current_balance: int,
            last_refill_date: date,
            tier: UserTier
    ) -> Dict[str, Any]:
        today = date.today()

        if last_refill_date >= today:
            return {
                "new_balance": current_balance,
                "refill_amount": 0,
                "should_update": False,
                "refill_date": last_refill_date
            }

        # Lấy policy dựa trên Tier
        policy = UserCreditPolicy.TIER_LIMITS.get(tier, UserCreditPolicy.TIER_LIMITS[UserTier.FREE])
        max_cap = policy["max_cap"]
        daily_amount = policy["daily_refill"]

        if current_balance >= max_cap:
            return {
                "new_balance": current_balance,
                "refill_amount": 0,
                "should_update": True,
                "refill_date": today
            }

        days_passed = (today - last_refill_date).days
        if days_passed <= 0:
            return {
                "new_balance": current_balance,
                "refill_amount": 0,
                "should_update": False,
                "refill_date": last_refill_date
            }

        total_refill = days_passed * daily_amount

        potential_balance = current_balance + total_refill
        new_balance = min(potential_balance, max_cap)

        real_refill_amount = new_balance - current_balance

        return {
            "new_balance": new_balance,
            "refill_amount": real_refill_amount,
            "should_update": True,
            "refill_date": today
        }