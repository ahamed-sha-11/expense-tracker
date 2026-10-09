from datetime import datetime
from decimal import Decimal

from pydantic import AwareDatetime, BaseModel, Field

from .models import TransactionType

class TransactionCreate(BaseModel):
    amount: Decimal = Field(gt=0, max_digits=12, decimal_places=2)
    transaction_type: TransactionType
    category: int = Field(gt=0)
    note: str | None = Field(default=None, max_length=80)
    transaction_date_time: AwareDatetime


class TransactionResponse(BaseModel):
    id: int
    amount: Decimal
    transaction_type: TransactionType
    category: int
    note: str | None
    transaction_date_time: datetime