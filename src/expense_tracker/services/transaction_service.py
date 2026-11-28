import math
from datetime import datetime

from sqlalchemy import func, select
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

from expense_tracker.exceptions.transaction import (
    InvalidDateRangeException,
    NegativeTransactionException,
    TransactionNotFoundException,
)
from expense_tracker.models.transaction import Transaction
from expense_tracker.models.types import TransactionType
from expense_tracker.schemas.transaction import (
    TransactionCreate,
    TransactionPageResponse,
    TransactionResponse,
    TransactionUpdate,
)
from expense_tracker.services import category_service


async def get_all_transactions(
    user_id: int,
    session: AsyncSession,
    page: int,
    size: int,
    transaction_type: TransactionType | None = None,
    category: int | None = None,
    start_date: datetime | None = None,
    end_date: datetime | None = None,
) -> TransactionPageResponse:
    if start_date is not None and end_date is not None and start_date > end_date:
        raise InvalidDateRangeException()

    # The same conditions are used for counting and for fetching the page,
    # so the total always matches the rows being paged through.
    conditions = [Transaction.user_id == user_id]

    # Each filter is optional. Every filter that is given narrows the results further (AND).
    if transaction_type is not None:
        conditions.append(Transaction.transaction_type == transaction_type)

    if category is not None:
        conditions.append(Transaction.category == category)

    # Dates are stored as Unix timestamps, so convert before comparing. Both ends are inclusive.
    if start_date is not None:
        start_timestamp = int(start_date.timestamp())
        conditions.append(Transaction.transaction_date_time >= start_timestamp)

    if end_date is not None:
        end_timestamp = int(end_date.timestamp())
        conditions.append(Transaction.transaction_date_time <= end_timestamp)

    count_statement = select(func.count(Transaction.id)).where(*conditions)
    total = await session.scalar(count_statement)

    offset = (page - 1) * size

    page_statement = (
        select(Transaction)
        .where(*conditions)
        .order_by(Transaction.transaction_date_time.desc(), Transaction.id.desc())
        .offset(offset)
        .limit(size)
    )

    result = await session.execute(page_statement)
    transactions = result.scalars().all()

    items = []
    for transaction in transactions:
        items.append(TransactionResponse.model_validate(transaction))

    total_pages = math.ceil(total / size)
    has_next = page < total_pages
    has_previous = page > 1

    return TransactionPageResponse(
        items=items,
        total=total,
        page=page,
        size=size,
        total_pages=total_pages,
        has_next=has_next,
        has_previous=has_previous,
    )

async def create_transaction(data: TransactionCreate, user_id: int, session: AsyncSession) -> Transaction:
    if data.amount <= 0:
        raise NegativeTransactionException(data.amount)

    await category_service.get_category_by_id(data.category, user_id, session)

    transaction_obj = Transaction(
        amount=data.amount,
        transaction_type=data.transaction_type,
        category=data.category,
        note=data.note,
        transaction_date_time=int(data.transaction_date_time.timestamp()),
        user_id=user_id,
    )

    session.add(transaction_obj)
    try:
        await session.commit()
    except SQLAlchemyError:
        await session.rollback()
        raise
    await session.refresh(transaction_obj)
    return transaction_obj


async def get_transaction_by_id(transaction_id: int, user_id: int, session: AsyncSession) -> Transaction:
    statement = select(Transaction).where(
        Transaction.id == transaction_id,
        Transaction.user_id == user_id,
    )

    transaction = await session.scalar(statement)
    if transaction is None:
        raise TransactionNotFoundException(transaction_id)

    return transaction

async def update_transaction(transaction_id: int, data: TransactionUpdate, user_id: int, session: AsyncSession) -> Transaction:
    transaction = await get_transaction_by_id(transaction_id, user_id, session)
    sent_fields = data.model_dump(exclude_unset=True)

    if "category" in sent_fields:
        await category_service.get_category_by_id(sent_fields["category"], user_id, session)

    for field, value in sent_fields.items():
        if field == "transaction_date_time":
            value = int(value.timestamp())

        setattr(transaction, field, value)

    try:
        await session.commit()
    except SQLAlchemyError:
        await session.rollback()
        raise
    await session.refresh(transaction)
    return transaction

async def delete_transaction(transaction_id: int, user_id: int, session: AsyncSession) -> None:
    transaction = await get_transaction_by_id(transaction_id, user_id, session)   # raises if not found

    await session.delete(transaction)
    try:
        await session.commit()
    except SQLAlchemyError:
        await session.rollback()
        raise
