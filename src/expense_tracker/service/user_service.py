from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

from expense_tracker.models import User
from expense_tracker.schemas import UserCreate
from expense_tracker.utils import hash_password


async def create_user(data : UserCreate, session : AsyncSession) -> User:

    email = data.email.lower()
    hashed_password = hash_password(data.password)

    user = User(
        email=email,
        username=data.username,
        password_hash=hashed_password,
    )

    session.add(user)
    try:
        await session.commit()
    except SQLAlchemyError:
        await session.rollback()
        raise

    await session.refresh(user)
    return user
