from sqlalchemy import BigInteger, Column, DateTime, ForeignKey, Integer, Numeric, String, func

from expense_tracker.core.database import Base
from expense_tracker.models.types import IntEnumType, TransactionType


class Transaction(Base):
    __tablename__ = "transactions"

    id = Column(Integer, primary_key=True, autoincrement=True)
    amount = Column(Numeric(12, 2), nullable=False)
    transaction_type = Column(IntEnumType(TransactionType), nullable=False)
    category = Column(Integer, ForeignKey("categories.id", ondelete="RESTRICT"), nullable=False)
    note = Column(String(80), nullable=True)
    transaction_date_time = Column(BigInteger, nullable=False)
    created_at = Column(DateTime, server_default=func.now(), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
