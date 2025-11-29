from enum import Enum


class UserTier(str, Enum):
    FREE = "free"
    PRO = "pro"