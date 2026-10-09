from decimal import Decimal
from pydantic import BaseModel, Field
from .models import TransactionType
from datetime import datetime

class TransactionCreate(BaseModel):
    amount: Decimal = Field(gt=0, max_digits=12, decimal_places=2)
    transaction_type: TransactionType
    category: int = Field(gt=0)
    note: str | None = Field(default=None, max_length=80)
    transaction_date_time: datetime