import datetime
from decimal import Decimal

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from expense_tracker.core.config import I_OWE_CATEGORY_ID, OWED_TO_ME_CATEGORY_ID
from expense_tracker.models.transaction import Transaction
from expense_tracker.models.types import TransactionType
from expense_tracker.schemas.transaction import CategoryTotal, DayTotal, MonthlyReportResponse

SETTLE_UP_CATEGORY_IDS = [OWED_TO_ME_CATEGORY_ID, I_OWE_CATEGORY_ID]


async def get_monthly_report(year: int, month: int, user_id: int, session: AsyncSession) -> MonthlyReportResponse:
    timezone = datetime.timezone.utc

    month_start = datetime.datetime(year, month, 1, tzinfo=timezone)
    if month == 12:
        next_month_start = datetime.datetime(year + 1, 1, 1, tzinfo=timezone)
    else:
        next_month_start = datetime.datetime(year, month + 1, 1, tzinfo=timezone)

    start_timestamp = int(month_start.timestamp())
    end_timestamp = int(next_month_start.timestamp())

    statement = select(Transaction).where(
        Transaction.user_id == user_id,
        Transaction.transaction_date_time >= start_timestamp,
        Transaction.transaction_date_time < end_timestamp,
    )
    result = await session.execute(statement)
    month_transactions = result.scalars().all()

    earned = Decimal("0")
    spent = Decimal("0")
    days = {}
    categories = {}

    for transaction in month_transactions:
        if transaction.category in SETTLE_UP_CATEGORY_IDS:
            continue

        local_time = datetime.datetime.fromtimestamp(transaction.transaction_date_time, tz=timezone)
        day = local_time.day
        if day not in days:
            days[day] = DayTotal(day=day, spent=Decimal("0"), earned=Decimal("0"))

        if transaction.transaction_type == TransactionType.EXPENSE:
            spent += transaction.amount
            days[day].spent += transaction.amount
            category_total = categories.get(transaction.category, Decimal("0"))
            categories[transaction.category] = category_total + transaction.amount
        else:
            earned += transaction.amount
            days[day].earned += transaction.amount

    day_list = [days[day] for day in sorted(days)]

    category_list = []
    for category_id, category_spent in categories.items():
        category_list.append(CategoryTotal(category=category_id, spent=category_spent))
    category_list.sort(key=lambda item: item.spent, reverse=True)

    owed_to_me, i_owe = await get_settle_up_balances(end_timestamp, user_id, session)

    return MonthlyReportResponse(
        year=year,
        month=month,
        earned=earned,
        spent=spent,
        left=earned - spent,
        days=day_list,
        categories=category_list,
        owed_to_me=owed_to_me,
        i_owe=i_owe,
    )


async def get_settle_up_balances(end_timestamp: int, user_id: int, session: AsyncSession) -> tuple[Decimal, Decimal]:
    statement = (
        select(Transaction.category, Transaction.transaction_type, func.sum(Transaction.amount))
        .where(
            Transaction.user_id == user_id,
            Transaction.category.in_(SETTLE_UP_CATEGORY_IDS),
            Transaction.transaction_date_time < end_timestamp,
        )
        .group_by(Transaction.category, Transaction.transaction_type)
    )
    result = await session.execute(statement)

    owed_to_me = Decimal("0")
    i_owe = Decimal("0")

    for category_id, transaction_type, total in result.all():
        total = Decimal(str(total))

        if category_id == OWED_TO_ME_CATEGORY_ID and transaction_type == TransactionType.EXPENSE:
            owed_to_me += total
        elif category_id == OWED_TO_ME_CATEGORY_ID and transaction_type == TransactionType.INCOME:
            owed_to_me -= total
        elif category_id == I_OWE_CATEGORY_ID and transaction_type == TransactionType.INCOME:
            i_owe += total
        elif category_id == I_OWE_CATEGORY_ID and transaction_type == TransactionType.EXPENSE:
            i_owe -= total

    return owed_to_me, i_owe
