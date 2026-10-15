import bcrypt
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from redis.asyncio import Redis
from sqlalchemy.ext.asyncio import AsyncSession

from expense_tracker.core.database import get_async_session, get_redis
from expense_tracker.models.user import User
from expense_tracker.services import session_service

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/users/login")


def hash_password(plain_password: str) -> str:
    return bcrypt.hashpw(plain_password.encode(), bcrypt.gensalt()).decode()


def verify_password(password: str, password_hash: str) -> bool:
        return bcrypt.checkpw(password.encode("utf-8"), password_hash.encode("utf-8"))


async def get_current_user(
    token: str = Depends(oauth2_scheme),
    redis: Redis = Depends(get_redis),
    session: AsyncSession = Depends(get_async_session),
) -> User:
    user_id = await session_service.get_session_user_id(token, redis)
    if user_id is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Session expired or invalid",
            headers={"WWW-Authenticate": "Bearer"},
        )

    user = await session.get(User, user_id)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Session expired or invalid",
            headers={"WWW-Authenticate": "Bearer"},
        )

    return user
