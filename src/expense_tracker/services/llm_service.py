from sqlalchemy import select
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

from expense_tracker.core.security import encrypt_api_key
from expense_tracker.exceptions.llm import LLMCredentialsAlreadyExistsException
from expense_tracker.models.llm import LLMCredentials
from expense_tracker.schemas.llm import LLMCredentialCreate, LLMCredentialResponse


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
