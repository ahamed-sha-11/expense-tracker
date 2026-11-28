from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from expense_tracker.core.database import get_async_session
from expense_tracker.core.security import get_current_user
from expense_tracker.exceptions.llm import (
    LLMCredentialsAlreadyExistsException,
    LLMCredentialsNotFoundException,
)
from expense_tracker.models.user import User
from expense_tracker.schemas.llm import (
    LLMCredentialCreate,
    LLMCredentialResponse,
    LLMCredentialUpdate,
)
from expense_tracker.services import llm_service

llm_router = APIRouter(
    prefix="/llm",
    tags=["llm"],
)

# Each user has at most one set of credentials, so the URLs need no id.


@llm_router.get("/credentials", response_model=LLMCredentialResponse)
async def get_llm_credentials(
    session: AsyncSession = Depends(get_async_session),
    current_user: User = Depends(get_current_user),
):
    try:
        return await llm_service.get_llm_credentials_response(current_user.id, session)
    except LLMCredentialsNotFoundException as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))


@llm_router.post("/credentials", response_model=LLMCredentialResponse, status_code=status.HTTP_201_CREATED)
async def save_llm_credentials(
    data: LLMCredentialCreate,
    session: AsyncSession = Depends(get_async_session),
    current_user: User = Depends(get_current_user),
):
    try:
        return await llm_service.save_llm_credentials(data, current_user.id, session)
    except LLMCredentialsAlreadyExistsException as e:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(e))


@llm_router.patch("/credentials", response_model=LLMCredentialResponse)
async def update_llm_credentials(
    data: LLMCredentialUpdate,
    session: AsyncSession = Depends(get_async_session),
    current_user: User = Depends(get_current_user),
):
    try:
        return await llm_service.update_llm_credentials(data, current_user.id, session)
    except LLMCredentialsNotFoundException as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))


@llm_router.delete("/credentials", status_code=status.HTTP_204_NO_CONTENT)
async def delete_llm_credentials(
    session: AsyncSession = Depends(get_async_session),
    current_user: User = Depends(get_current_user),
):
    try:
        await llm_service.delete_llm_credentials(current_user.id, session)
    except LLMCredentialsNotFoundException as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
