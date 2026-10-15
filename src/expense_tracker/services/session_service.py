import secrets

from redis.asyncio import Redis

from expense_tracker.core.config import SESSION_TTL_SECONDS


async def create_session(user_id: int, redis: Redis) -> str:
    token = secrets.token_urlsafe(32)
    key = f"session:{token}"

    await redis.set(key, user_id, ex=SESSION_TTL_SECONDS)
    return token


async def get_session_user_id(token: str, redis: Redis) -> int | None:
    key = f"session:{token}"

    user_id = await redis.get(key)
    if user_id is None:
        return None

    return int(user_id)


async def delete_session(token: str, redis: Redis) -> None:
    key = f"session:{token}"

    await redis.delete(key)
