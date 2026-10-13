from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from expense_tracker.config.database import get_async_session
from expense_tracker.schemas import UserCreate, UserResponse
from expense_tracker.service import user_service

user_router= APIRouter(
    prefix="/users",
    tags=["users"]
)

@user_router.get("/me")
async def get_current_user():
    pass

@user_router.post("/", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def create_user(data: UserCreate, session: AsyncSession = Depends(get_async_session)):
    try:
        return await user_service.create_user(data, session)
    except IntegrityError:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Email or username already exists")
