from dataclasses import field
from datetime import date
from typing import Optional

from pydantic import BaseModel, ConfigDict


class UserCredit(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: Optional[int] = None
    user_id: int
    balance: int = field(default=5)
    last_refill_processed_date: Optional[date] = None