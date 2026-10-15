
from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

from expense_tracker.exceptions.transaction import NegativeTransactionException, TransactionNotFoundException
from expense_tracker.models.transaction import Transaction
from expense_tracker.schemas.transaction import TransactionCreate, TransactionUpdate
from expense_tracker.services import category_service


async def get_all_transactions(user_id: int, session: AsyncSession, page: int, size: int) -> list[Transaction]:
    offset = (page - 1) * size

    statement = (
        select(Transaction)
        .where(Transaction.user_id == user_id)
        .order_by(Transaction.transaction_date_time.desc(), Transaction.id.desc())
        .offset(offset)
        .limit(size)
    )

    result = await session.execute(statement)
    return list(result.scalars().all())

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
    sent_fields = data.model_dump(exclude_none=True)

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
