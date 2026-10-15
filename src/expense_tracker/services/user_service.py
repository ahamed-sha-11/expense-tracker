import asyncio

from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

from expense_tracker.exceptions.user import InvalidCredentialsException
from expense_tracker.models.user import User
from expense_tracker.schemas.user import UserCreate
from expense_tracker.core.security import hash_password, verify_password


async def create_user(data : UserCreate, session : AsyncSession) -> User:

    email = data.email.lower()
    hashed_password = await asyncio.to_thread(hash_password, data.password)

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


async def authenticate(email: str, password: str, session: AsyncSession) -> User:
    email = email.lower()

    statement = select(User).where(User.email == email)
    user = await session.scalar(statement)
    if user is None:
        raise InvalidCredentialsException()

    password_matches = await asyncio.to_thread(verify_password, password, user.password_hash)
    if not password_matches:
        raise InvalidCredentialsException()

    return user
