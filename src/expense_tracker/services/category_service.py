from sqlalchemy import or_, select
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

from expense_tracker.core.config import DEFAULT_CATEGORY_ID, DEFAULT_CATEGORY_NAME
from expense_tracker.exceptions.category import (
    CategoryInUseException,
    CategoryNotFoundException,
    SystemCategoryModificationException,
)
from expense_tracker.models.category import Category
from expense_tracker.models.transaction import Transaction
from expense_tracker.schemas.category import CategoryCreate, CategoryUpdate


async def ensure_default_category(session: AsyncSession) -> None:
    if await session.get(Category, DEFAULT_CATEGORY_ID) is None:
        session.add(Category(id=DEFAULT_CATEGORY_ID, name=DEFAULT_CATEGORY_NAME))
        await session.commit()


async def create_category(data: CategoryCreate, user_id: int, session: AsyncSession) -> Category:
    category_name = data.name.lower().capitalize()
    category_obj = Category(
        name=category_name,
        user_id=user_id,
    )

    session.add(category_obj)
    try:
        await session.commit()
    except SQLAlchemyError:
        await session.rollback()
        raise
    await session.refresh(category_obj)
    return category_obj

async def get_all_categories(user_id: int, session: AsyncSession, page: int, size: int) -> list[Category]:
    offset = (page - 1) * size

    statement = (
        select(Category)
        .where(or_(Category.user_id == user_id, Category.user_id.is_(None)))
        .order_by(Category.name)
        .offset(offset)
        .limit(size)
    )

    result = await session.execute(statement)
    return list(result.scalars().all())

async def get_category_by_id(category_id: int, user_id: int, session: AsyncSession) -> Category:
    statement = select(Category).where(
        Category.id == category_id,
        or_(Category.user_id == user_id, Category.user_id.is_(None)),
    )

    category = await session.scalar(statement)
    if category is None:
        raise CategoryNotFoundException(category_id)

    return category


async def update_category(category_id: int, data: CategoryUpdate, user_id: int, session: AsyncSession) -> Category:
    category = await get_category_by_id(category_id, user_id, session)

    if category.user_id is None:
        raise SystemCategoryModificationException(category_id)

    category.name = data.name.lower().capitalize()

    try:
        await session.commit()
    except SQLAlchemyError:
        await session.rollback()
        raise
    await session.refresh(category)
    return category


async def delete_category(category_id: int, user_id: int, session: AsyncSession) -> None:
    category = await get_category_by_id(category_id, user_id, session)

    if category.user_id is None:
        raise SystemCategoryModificationException(category_id)

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
