from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

from expense_tracker.security.configs import hash_password
from expense_tracker.users.models import User
from expense_tracker.users.schemas import UserCreate, UserDto


async def create_user(data : UserCreate, session : AsyncSession) -> UserDto:

    hashed_password = hash_password(data.password)

    user = User(
        email=data.email,
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
    user_dto = UserDto.model_validate(user)
    return user_dto