from datetime import datetime
from decimal import Decimal

from pydantic import AwareDatetime, BaseModel, EmailStr, Field, field_validator

from expense_tracker.config.config import ALLOWED_PASSWORD_CHARACTERS
from expense_tracker.models import TransactionType


class CategoryCreate(BaseModel):
    name: str = Field(min_length=1, max_length=80)

class CategoryUpdate(BaseModel):
    name: str = Field(min_length=1, max_length=80)

class CategoryResponse(BaseModel):
    id: int
    name: str


class TransactionCreate(BaseModel):
    amount: Decimal = Field(gt=0, max_digits=12, decimal_places=2)
    transaction_type: TransactionType
    category: int = Field(gt=0)
    note: str | None = Field(default=None, max_length=80)
    transaction_date_time: AwareDatetime

class TransactionUpdate(BaseModel):
    amount: Decimal | None = Field(default=None, gt=0, max_digits=12, decimal_places=2)
    transaction_type: TransactionType | None = None
    category: int | None = Field(default=None, gt=0)
    note: str | None = Field(default=None, max_length=80)
    transaction_date_time: AwareDatetime | None = None


class TransactionResponse(BaseModel):
    id: int
    amount: Decimal
    transaction_type: TransactionType
    category: int
    note: str | None
    transaction_date_time: datetime


class UserResponse(BaseModel):
    username: str
    email: EmailStr


class UserCreate(BaseModel):
    email: EmailStr
    username: str = Field(min_length=3, max_length=50)
    password: str = Field(min_length=8, max_length=20)

    @field_validator("password")
    @classmethod
    def check_password_characters(cls, password: str) -> str:
        for character in password:
            if character not in ALLOWED_PASSWORD_CHARACTERS:
                raise ValueError("Password can only contain letters, digits and symbols like !@#$%^&*")
        return password
