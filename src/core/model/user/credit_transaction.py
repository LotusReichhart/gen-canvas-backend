from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict

from .enums.credit_transaction_source import CreditTransactionSource


class CreditTransaction(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: Optional[int] = None
    credit_id: int
    amount: int
    source: CreditTransactionSource
    created_at: datetime
    balance_after: int