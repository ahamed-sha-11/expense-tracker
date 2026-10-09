import enum

from sqlalchemy import BigInteger, Column, DateTime, ForeignKey, Integer, Numeric, String, TypeDecorator, func
from expense_tracker.db import Base

class TransactionType(enum.IntEnum):
    INCOME = 1
    EXPENSE = 2


class IntEnumType(TypeDecorator):
    impl = Integer
    cache_ok = True

    def __init__(self, enum_type):
        super().__init__()
        self.enum_type = enum_type

    def process_bind_param(self, value, dialect):
        if value is None:
            return None
        return int(value)

    def process_result_value(self, value, dialect):
        if value is None:
            return None
        return self.enum_type(value)


class Transaction(Base):
    __tablename__ = "transactions"

    id = Column(Integer, primary_key=True, autoincrement=True)
    amount = Column(Numeric(12, 2), nullable=False)
    transaction_type = Column(IntEnumType(TransactionType), nullable=False)
    category = Column(Integer, ForeignKey("categories.id", ondelete="RESTRICT"), nullable=False)
    note = Column(String(80), nullable=True)
    transaction_date_time = Column(BigInteger, nullable=False)
    created_at = Column(DateTime, server_default=func.now(), nullable=False)
