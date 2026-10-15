from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from redis.asyncio import Redis
from expense_tracker.core.database import get_async_session, get_redis
from expense_tracker.exceptions.user import InvalidCredentialsException
from expense_tracker.models.user import User
from expense_tracker.core.security import get_current_user, oauth2_scheme
from expense_tracker.schemas.user import UserCreate, UserResponse
from expense_tracker.services import session_service, user_service

user_router= APIRouter(
    prefix="/users",
    tags=["users"]
)

@user_router.get("/me", response_model=UserResponse)
async def read_current_user(current_user: User = Depends(get_current_user)):
    return current_user

@user_router.post("/", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def create_user(data: UserCreate, session: AsyncSession = Depends(get_async_session)):
    try:
        return await user_service.create_user(data, session)
    except IntegrityError:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Email or username already exists")

@user_router.post("/login")
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    session: AsyncSession = Depends(get_async_session),
    redis: Redis = Depends(get_redis),
):
    try:
        user = await user_service.authenticate(form_data.username, form_data.password, session)
    except InvalidCredentialsException as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=str(e),
            headers={"WWW-Authenticate": "Bearer"},
        )

    token = await session_service.create_session(user.id, redis)
    return {"access_token": token, "token_type": "bearer"}

@user_router.post("/logout", status_code=status.HTTP_204_NO_CONTENT, dependencies=[Depends(get_current_user)])
async def logout(token: str = Depends(oauth2_scheme), redis: Redis = Depends(get_redis)):
    await session_service.delete_session(token, redis)

@user_router.get("/redis-check")
async def redis_check(redis: Redis = Depends(get_redis)):
    return {"redis": await redis.ping()}
