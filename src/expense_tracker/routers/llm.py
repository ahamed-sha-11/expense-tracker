from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from expense_tracker.core.database import get_async_session
from expense_tracker.core.security import get_current_user
from expense_tracker.exceptions.llm import LLMCredentialsAlreadyExistsException
from expense_tracker.models.user import User
from expense_tracker.schemas.llm import LLMCredentialCreate, LLMCredentialResponse
from expense_tracker.services import llm_service

llm_router = APIRouter(
    prefix="/llm",
    tags=["llm"],
)


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
