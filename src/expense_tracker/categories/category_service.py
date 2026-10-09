from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

from expense_tracker.categories.exceptions import CategoryNotFoundException
from expense_tracker.categories.models import Category
from expense_tracker.categories.schemas import CategoryCreate


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


async def get_category_by_id(category_id: int, session: AsyncSession) -> Category:
    category = await session.get(Category, category_id)
    if category is None:
        raise CategoryNotFoundException(category_id)

    return category
