from datetime import datetime
from decimal import Decimal

from pydantic import AwareDatetime, BaseModel, ConfigDict, Field, field_validator

from expense_tracker.core.config import DEFAULT_CATEGORY_ID
from expense_tracker.models.types import TransactionType


class TransactionCreate(BaseModel):
    amount: Decimal = Field(gt=0, max_digits=12, decimal_places=2)
    transaction_type: TransactionType
    category: int = Field(default=DEFAULT_CATEGORY_ID, ge=-3)
    note: str | None = Field(default=None, max_length=80)
    transaction_date_time: AwareDatetime

class TransactionUpdate(BaseModel):
    amount: Decimal | None = Field(default=None, gt=0, max_digits=12, decimal_places=2)
    transaction_type: TransactionType | None = None
    category: int | None = Field(default=None, ge=-3)
    note: str | None = Field(default=None, max_length=80)
    transaction_date_time: AwareDatetime | None = None

    @field_validator("amount", "transaction_type", "category", "transaction_date_time")
    @classmethod
    def reject_null(cls, value):
        if value is None:
            raise ValueError("Can't be empty. Leave the field out to keep its current value")
        return value


class TransactionResponse(BaseModel):
    # Lets the service build this response straight from a Transaction database object
    model_config = ConfigDict(from_attributes=True)

    id: int
    amount: Decimal
    transaction_type: TransactionType
    category: int
    note: str | None
    transaction_date_time: datetime


class TransactionPageResponse(BaseModel):
    items: list[TransactionResponse]
    total: int            # how many transactions match the filters, across all pages
    page: int             # the page number returned
    size: int             # the most items a page can hold
    total_pages: int      # 0 when nothing matches
    has_next: bool
    has_previous: bool


class DayTotal(BaseModel):
    day: int
    spent: Decimal
    earned: Decimal


class CategoryTotal(BaseModel):
    category: int
    spent: Decimal


class MonthlyReportResponse(BaseModel):
    year: int
    month: int
    earned: Decimal
    spent: Decimal
    left: Decimal
    days: list[DayTotal]
    categories: list[CategoryTotal]
    owed_to_me: Decimal
    i_owe: Decimal

class MonthOnMonthComparisonResponse(BaseModel):
    year: int
    month_one: int
    month_two: int

    month_one_income: Decimal
    month_two_income: Decimal
    income_difference: Decimal

    month_one_expense: Decimal
    month_two_expense: Decimal
    expense_difference: Decimal

    # None when the month has no income, because a percentage of zero income has no meaning
    month_one_spend_percentage: float | None
    month_two_spend_percentage: float | None
    spend_percentage_difference: float | None

    month_one_savings_percentage: float | None
    month_two_savings_percentage: float | None
    savings_percentage_difference: float | None