from sqlalchemy import or_, select
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

from expense_tracker.core.config import (
    DEFAULT_CATEGORY_ID,
    DEFAULT_CATEGORY_NAME,
    I_OWE_CATEGORY_ID,
    I_OWE_CATEGORY_NAME,
    OWED_TO_ME_CATEGORY_ID,
    OWED_TO_ME_CATEGORY_NAME,
)
from expense_tracker.exceptions.category import (
    CategoryAlreadyExistsException,
    CategoryInUseException,
    CategoryNotFoundException,
    SystemCategoryModificationException,
)
from expense_tracker.models.category import Category
from expense_tracker.models.transaction import Transaction
from expense_tracker.schemas.category import CategoryCreate, CategoryUpdate


async def ensure_default_categories(session: AsyncSession) -> None:
    default_categories = [
        (DEFAULT_CATEGORY_ID, DEFAULT_CATEGORY_NAME),
        (OWED_TO_ME_CATEGORY_ID, OWED_TO_ME_CATEGORY_NAME),
        (I_OWE_CATEGORY_ID, I_OWE_CATEGORY_NAME),
    ]

    for category_id, category_name in default_categories:
        if await session.get(Category, category_id) is None:
            session.add(Category(id=category_id, name=category_name))

    await session.commit()


async def ensure_category_name_available(
    category_name: str,
    user_id: int,
    session: AsyncSession,
    current_category_id: int | None = None,
) -> None:
    # A name is taken if the user already has it, or if a default category uses it
    statement = select(Category.id).where(
        Category.name == category_name,
        or_(Category.user_id == user_id, Category.user_id.is_(None)),
    )

    # When renaming, the category's own current name does not count as taken
    if current_category_id is not None:
        statement = statement.where(Category.id != current_category_id)

    existing_category_id = await session.scalar(statement)
    if existing_category_id is not None:
        raise CategoryAlreadyExistsException(category_name)


async def create_category(data: CategoryCreate, user_id: int, session: AsyncSession) -> Category:
    category_name = data.name.lower().capitalize()
    await ensure_category_name_available(category_name, user_id, session)

    category_obj = Category(
        name=category_name,
        user_id=user_id,
    )

    session.add(category_obj)
    try:
        await session.commit()
    except IntegrityError:
        # Two requests with the same name at the same time: the unique constraint catches the second one
        await session.rollback()
        raise CategoryAlreadyExistsException(category_name)
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

    category_name = data.name.lower().capitalize()
    await ensure_category_name_available(category_name, user_id, session, category_id)

    category.name = category_name

    try:
        await session.commit()
    except IntegrityError:
        await session.rollback()
        raise CategoryAlreadyExistsException(category_name)
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
