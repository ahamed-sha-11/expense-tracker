from datetime import datetime
from decimal import Decimal

from pydantic import AwareDatetime, BaseModel, Field

from expense_tracker.core.config import DEFAULT_CATEGORY_ID
from expense_tracker.models.types import TransactionType


class TransactionCreate(BaseModel):
    amount: Decimal = Field(gt=0, max_digits=12, decimal_places=2)
    transaction_type: TransactionType
    category: int = Field(default=DEFAULT_CATEGORY_ID, ge=-1)
    note: str | None = Field(default=None, max_length=80)
    transaction_date_time: AwareDatetime

class TransactionUpdate(BaseModel):
    amount: Decimal | None = Field(default=None, gt=0, max_digits=12, decimal_places=2)
    transaction_type: TransactionType | None = None
    category: int | None = Field(default=None, ge=-1)
    note: str | None = Field(default=None, max_length=80)
    transaction_date_time: AwareDatetime | None = None


class TransactionResponse(BaseModel):
    id: int
    amount: Decimal
    transaction_type: TransactionType
    category: int
    note: str | None
    transaction_date_time: datetime
