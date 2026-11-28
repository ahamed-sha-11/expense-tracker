from sqlalchemy import select
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

from expense_tracker.core.security import encrypt_api_key
from expense_tracker.exceptions.llm import (
    LLMCredentialsAlreadyExistsException,
    LLMCredentialsNotFoundException,
)
from expense_tracker.models.llm import LLMCredentials
from expense_tracker.schemas.llm import (
    LLMCredentialCreate,
    LLMCredentialResponse,
    LLMCredentialUpdate,
)


async def save_llm_credentials(
    data: LLMCredentialCreate,
    user_id: int,
    session: AsyncSession,
) -> LLMCredentialResponse:
    # Each user can save one set of credentials (user_id is unique in the table)
    statement = select(LLMCredentials).where(LLMCredentials.user_id == user_id)
    existing_credentials = await session.scalar(statement)

    if existing_credentials is not None:
        raise LLMCredentialsAlreadyExistsException(user_id)

    encrypted_api_key, nonce = encrypt_api_key(data.api_key)
    mask = mask_api_key(data.api_key)

    llm_credential = LLMCredentials(
        user_id=user_id,
        encrypted_api_key=encrypted_api_key,
        nonce=nonce,
        mask=mask,
        model=data.model,
    )

    session.add(llm_credential)
    try:
        await session.commit()
    except IntegrityError:
        # Two save requests at the same time: the unique constraint catches the second one
        await session.rollback()
        raise LLMCredentialsAlreadyExistsException(user_id)
    except SQLAlchemyError:
        await session.rollback()
        raise
    await session.refresh(llm_credential)

    return build_response(llm_credential)


async def get_llm_credentials(user_id: int, session: AsyncSession) -> LLMCredentials:
    statement = select(LLMCredentials).where(LLMCredentials.user_id == user_id)
    llm_credential = await session.scalar(statement)

    if llm_credential is None:
        raise LLMCredentialsNotFoundException(user_id)

    return llm_credential


async def get_llm_credentials_response(user_id: int, session: AsyncSession) -> LLMCredentialResponse:
    llm_credential = await get_llm_credentials(user_id, session)   # raises if not found
    return build_response(llm_credential)


async def update_llm_credentials(
    data: LLMCredentialUpdate,
    user_id: int,
    session: AsyncSession,
) -> LLMCredentialResponse:
    llm_credential = await get_llm_credentials(user_id, session)   # raises if not found
    sent_fields = data.model_dump(exclude_unset=True)

    if "api_key" in sent_fields:
        # A new key gets a new nonce. AES-GCM must never reuse a nonce with the same encryption key.
        encrypted_api_key, nonce = encrypt_api_key(sent_fields["api_key"])
        llm_credential.encrypted_api_key = encrypted_api_key
        llm_credential.nonce = nonce
        llm_credential.mask = mask_api_key(sent_fields["api_key"])

    if "model" in sent_fields:
        llm_credential.model = sent_fields["model"]

    if "is_active" in sent_fields:
        llm_credential.is_active = sent_fields["is_active"]

    try:
        await session.commit()
    except SQLAlchemyError:
        await session.rollback()
        raise
    await session.refresh(llm_credential)

    return build_response(llm_credential)


async def delete_llm_credentials(user_id: int, session: AsyncSession) -> None:
    llm_credential = await get_llm_credentials(user_id, session)   # raises if not found

    await session.delete(llm_credential)
    try:
        await session.commit()
    except SQLAlchemyError:
        await session.rollback()
        raise


def build_response(llm_credential: LLMCredentials) -> LLMCredentialResponse:
    # Only the masked key leaves the server, never the real one
    return LLMCredentialResponse(
        id=llm_credential.id,
        masked_key=llm_credential.mask,
        model=llm_credential.model,
        is_active=llm_credential.is_active,
    )


def mask_api_key(api_key: str) -> str:
    first_part = api_key[:4]
    last_part = api_key[-4:]
    return first_part + "*" * 8 + last_part
