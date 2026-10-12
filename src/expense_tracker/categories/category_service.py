from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

from expense_tracker.categories.exceptions import CategoryInUseException, CategoryNotFoundException
from expense_tracker.categories.models import Category
from expense_tracker.categories.schemas import CategoryCreate, CategoryUpdate
from expense_tracker.constants import DEFAULT_CATEGORY_ID, DEFAULT_CATEGORY_NAME
from expense_tracker.transactions.models import Transaction


async def ensure_default_category(session: AsyncSession) -> None:
    if await session.get(Category, DEFAULT_CATEGORY_ID) is None:
        session.add(Category(id=DEFAULT_CATEGORY_ID, name=DEFAULT_CATEGORY_NAME))
        await session.commit()


async def create_category(data: CategoryCreate, session: AsyncSession) -> Category:
    category_name = data.name.lower().capitalize()
    category_obj = Category(
        name=category_name,
    )

    session.add(category_obj)
    try:
        await session.commit()
    except SQLAlchemyError:
        await session.rollback()
        raise
    await session.refresh(category_obj)
    return category_obj

async def get_all_categories(session: AsyncSession, page: int, size: int) -> list[Category]:
    offset = (page - 1) * size

    statement = (
        select(Category)
        .order_by(Category.name)
        .offset(offset)
        .limit(size)
    )

    result = await session.execute(statement)
    return list(result.scalars().all())

async def get_category_by_id(category_id: int, session: AsyncSession) -> Category:
    category = await session.get(Category, category_id)
    if category is None:
        raise CategoryNotFoundException(category_id)

    return category


async def update_category(category_id: int, data: CategoryUpdate, session: AsyncSession) -> Category:
    category = await get_category_by_id(category_id, session)

    category.name = data.name.lower().capitalize()

    try:
        await session.commit()
    except SQLAlchemyError:
        await session.rollback()
        raise
    await session.refresh(category)
    return category


async def delete_category(category_id: int, session: AsyncSession) -> None:
    category = await get_category_by_id(category_id, session)

    in_use = await session.scalar(
        select(Transaction.id).where(Transaction.category == category_id).limit(1)
    )

    if in_use is not None:
        raise CategoryInUseException(category_id)

    await session.delete(category)
    try:
        await session.commit()
    except SQLAlchemyError:
        await session.rollback()
        raise