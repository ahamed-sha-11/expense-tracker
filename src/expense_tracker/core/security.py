import os
import bcrypt

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from redis.asyncio import Redis
from sqlalchemy.ext.asyncio import AsyncSession
from cryptography.hazmat.primitives.ciphers.aead import AESGCM

from expense_tracker.core.database import get_async_session, get_redis
from expense_tracker.models.user import User
from expense_tracker.services import session_service


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/users/login")


def get_encryption_key() -> bytes:
    encryption_key = os.getenv("LLM_ENCRYPTION_KEY")

    if not encryption_key:
        raise RuntimeError("LLM_ENCRYPTION_KEY is not configured")

    key = bytes.fromhex(encryption_key)

    if len(key) != 32:
        raise ValueError("LLM encryption key must be 32 bytes")

    return key


def hash_password(plain_password: str) -> str:
    return bcrypt.hashpw(
        plain_password.encode("utf-8"),
        bcrypt.gensalt()
    ).decode("utf-8")


def verify_password(password: str, password_hash: str) -> bool:
    return bcrypt.checkpw(
        password.encode("utf-8"),
        password_hash.encode("utf-8")
    )


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


def encrypt_api_key(api_key: str) -> tuple[bytes, bytes]:
    aes = AESGCM(get_encryption_key())
    nonce = os.urandom(12)

    encrypted_api_key = aes.encrypt(
        nonce,
        api_key.encode("utf-8"),
        None
    )

    return encrypted_api_key, nonce


def decrypt_api_key(
    encrypted_api_key: bytes,
    nonce: bytes
) -> str:
    aes = AESGCM(get_encryption_key())

    decrypted_api_key = aes.decrypt(
        nonce,
        encrypted_api_key,
        None
    )

    return decrypted_api_key.decode("utf-8")
