
import datetime
from decimal import Decimal

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from expense_tracker.core.config import (
    I_OWE_CATEGORY_ID,
    OWED_TO_ME_CATEGORY_ID,
)
from expense_tracker.models.transaction import Transaction
from expense_tracker.models.types import TransactionType
from expense_tracker.schemas.transaction import (
    CategoryTotal,
    DayTotal,
    MonthOnMonthComparisonResponse,
    MonthlyReportResponse,
)


SETTLE_UP_CATEGORY_IDS = [
    OWED_TO_ME_CATEGORY_ID,
    I_OWE_CATEGORY_ID,
]


async def get_monthly_report(
    year: int,
    month: int,
    user_id: int,
    session: AsyncSession,
) -> MonthlyReportResponse:
    timezone = datetime.timezone.utc

    month_start = datetime.datetime(
        year, month, 1, tzinfo=timezone
    )

    if month == 12:
        next_month_start = datetime.datetime(
            year + 1, 1, 1, tzinfo=timezone
        )
    else:
        next_month_start = datetime.datetime(
            year, month + 1, 1, tzinfo=timezone
        )

    start_timestamp = int(month_start.timestamp())
    end_timestamp = int(next_month_start.timestamp())

    statement = select(Transaction).where(
        Transaction.user_id == user_id,
        Transaction.transaction_date_time >= start_timestamp,
        Transaction.transaction_date_time < end_timestamp,
        Transaction.category.notin_(SETTLE_UP_CATEGORY_IDS),
    )

    result = await session.execute(statement)
    transactions = result.scalars().all()

    earned = Decimal("0")
    spent = Decimal("0")

    days: dict[int, DayTotal] = {}
    categories: dict[int, Decimal] = {}

    for transaction in transactions:
        transaction_time = datetime.datetime.fromtimestamp(
            transaction.transaction_date_time,
            tz=timezone,
        )

        day = transaction_time.day

        if day not in days:
            days[day] = DayTotal(
                day=day,
                spent=Decimal("0"),
                earned=Decimal("0"),
            )

        if transaction.transaction_type == TransactionType.EXPENSE:
            spent += transaction.amount
            days[day].spent += transaction.amount

            if transaction.category not in categories:
                categories[transaction.category] = Decimal("0")

            categories[transaction.category] += transaction.amount

        else:
            earned += transaction.amount
            days[day].earned += transaction.amount

    day_list = sorted(
        days.values(),
        key=lambda item: item.day,
    )

    category_list = [
        CategoryTotal(category=category_id, spent=amount)
        for category_id, amount in categories.items()
    ]

    category_list.sort(
        key=lambda item: item.spent,
        reverse=True,
    )

    owed_to_me, i_owe = await get_settle_up_balances(
        end_timestamp,
        user_id,
        session,
    )

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


async def get_settle_up_balances(
    end_timestamp: int,
    user_id: int,
    session: AsyncSession,
) -> tuple[Decimal, Decimal]:
    statement = (
        select(
            Transaction.category,
            Transaction.transaction_type,
            func.sum(Transaction.amount),
        )
        .where(
            Transaction.user_id == user_id,
            Transaction.category.in_(SETTLE_UP_CATEGORY_IDS),
            Transaction.transaction_date_time < end_timestamp,
        )
        .group_by(
            Transaction.category,
            Transaction.transaction_type,
        )
    )

    result = await session.execute(statement)

    owed_to_me = Decimal("0")
    i_owe = Decimal("0")

    for category_id, transaction_type, total in result.all():
        total = Decimal(str(total))

        if (
            category_id == OWED_TO_ME_CATEGORY_ID
            and transaction_type == TransactionType.EXPENSE
        ):
            owed_to_me += total

        elif (
            category_id == OWED_TO_ME_CATEGORY_ID
            and transaction_type == TransactionType.INCOME
        ):
            owed_to_me -= total

        elif (
            category_id == I_OWE_CATEGORY_ID
            and transaction_type == TransactionType.INCOME
        ):
            i_owe += total

        elif (
            category_id == I_OWE_CATEGORY_ID
            and transaction_type == TransactionType.EXPENSE
        ):
            i_owe -= total

    return owed_to_me, i_owe


async def get_month_on_month_comparison(
    year: int,
    month_one: int,
    month_two: int,
    user_id: int,
    session: AsyncSession,
) -> MonthOnMonthComparisonResponse:
    month_one, month_two = min(month_one, month_two), max(month_one, month_two)

    month_one_report = await get_monthly_report(
        year,
        month_one,
        user_id,
        session,
    )

    month_two_report = await get_monthly_report(
        year,
        month_two,
        user_id,
        session,
    )

    return get_monthly_diff(
        month_one_report,
        month_two_report,
    )


def get_monthly_diff(
    month_one_report: MonthlyReportResponse,
    month_two_report: MonthlyReportResponse,
) -> MonthOnMonthComparisonResponse:
    year = month_one_report.year
    month_one = month_one_report.month
    month_two = month_two_report.month

    month_one_income = month_one_report.earned
    month_two_income = month_two_report.earned
    income_difference = month_two_income - month_one_income

    month_one_expense = month_one_report.spent
    month_two_expense = month_two_report.spent
    expense_difference = month_two_expense - month_one_expense

    month_one_spend_percentage = (
        float(month_one_expense / month_one_income * 100)
        if month_one_income > 0
        else 0.0
    )

    month_two_spend_percentage = (
        float(month_two_expense / month_two_income * 100)
        if month_two_income > 0
        else 0.0
    )

    spend_percentage_difference = (
        month_two_spend_percentage - month_one_spend_percentage
    )

    month_one_savings_percentage = (
        float(
            (month_one_income - month_one_expense)
            / month_one_income * 100
        )
        if month_one_income > 0
        else 0.0
    )

    month_two_savings_percentage = (
        float(
            (month_two_income - month_two_expense)
            / month_two_income * 100
        )
        if month_two_income > 0
        else 0.0
    )

    savings_percentage_difference = (
        month_two_savings_percentage - month_one_savings_percentage
    )

    return MonthOnMonthComparisonResponse(
        year=year,
        month_one=month_one,
        month_two=month_two,
        month_one_income=month_one_income,
        month_two_income=month_two_income,
        income_difference=income_difference,
        month_one_expense=month_one_expense,
        month_two_expense=month_two_expense,
        expense_difference=expense_difference,
        month_one_spend_percentage=month_one_spend_percentage,
        month_two_spend_percentage=month_two_spend_percentage,
        spend_percentage_difference=spend_percentage_difference,
        month_one_savings_percentage=month_one_savings_percentage,
        month_two_savings_percentage=month_two_savings_percentage,
        savings_percentage_difference=savings_percentage_difference,
    )
