from src.core.model.user.enums.user_tier import UserTier


class UserCreditPolicy:
    TIER_LIMITS = {
        UserTier.FREE: {"max_cap": 10, "daily_refill": 3},
        UserTier.PRO: {"max_cap": 60, "daily_refill": 20},
    }
