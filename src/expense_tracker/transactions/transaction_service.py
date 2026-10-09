
from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession
from expense_tracker.categories.exceptions import CategoryNotFoundException
from expense_tracker.categories.models import Category
from expense_tracker.transactions.exceptions import NegativeTransactionException, TransactionNotFoundException
from expense_tracker.transactions.models import Transaction
from expense_tracker.transactions.schemas import TransactionCreate, TransactionUpdate


async def get_all_transactions(session: AsyncSession, page: int, size: int) -> list[Transaction]:
    offset = (page - 1) * size

    statement = (
        select(Transaction)
        .order_by(Transaction.transaction_date_time.desc(), Transaction.id.desc())
        .offset(offset)
        .limit(size)
    )

    result = await session.execute(statement)
    return list(result.scalars().all())

async def create_transaction(data: TransactionCreate, session: AsyncSession) -> Transaction:
    if data.amount <= 0:
        raise NegativeTransactionException(data.amount)

    if await session.get(Category, data.category) is None:
        raise CategoryNotFoundException(data.category)

    transaction_obj = Transaction(
        amount=data.amount,
        transaction_type=data.transaction_type,
        category=data.category,
        note=data.note,
        transaction_date_time=int(data.transaction_date_time.timestamp()),
    )

    session.add(transaction_obj)
    try:
        await session.commit()
    except SQLAlchemyError:
        await session.rollback()
        raise
    await session.refresh(transaction_obj)
    return transaction_obj


async def get_transaction_by_id(transaction_id: int, session: AsyncSession) -> Transaction:

    transaction = await session.get(Transaction, transaction_id)
    if transaction is None:
        raise TransactionNotFoundException(transaction_id)

    return transaction

async def update_transaction(transaction_id: int, data: TransactionUpdate, session: AsyncSession) -> Transaction:

    transaction = await get_transaction_by_id(transaction_id, session)
    sent_fields = data.model_dump(exclude_unset=True)

    for field, value in sent_fields.items():
        if field == "transaction_date_time":
            value = int(value.timestamp())

        setattr(transaction, field, value)

    await session.commit()
    await session.refresh(transaction)
    return transaction