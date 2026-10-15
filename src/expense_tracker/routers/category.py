from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.ext.asyncio import AsyncSession

from expense_tracker.core.database import get_async_session
from expense_tracker.core.security import get_current_user
from expense_tracker.exceptions.category import (
    CategoryInUseException,
    CategoryNotFoundException,
    SystemCategoryModificationException,
)
from expense_tracker.models.user import User
from expense_tracker.schemas.category import CategoryCreate, CategoryResponse, CategoryUpdate
from expense_tracker.services import category_service

category_router = APIRouter(
    prefix="/categories",
    tags=["categories"],
)


@category_router.get("/", response_model=list[CategoryResponse])
async def get_all_categories(
        page: int = Query(1, ge=1),
        size: int = Query(100, ge=1, le=100),
        session: AsyncSession = Depends(get_async_session),
        current_user: User = Depends(get_current_user),
):
    return await category_service.get_all_categories(current_user.id, session, page, size)


@category_router.post("/", response_model=CategoryResponse, status_code=status.HTTP_201_CREATED)
async def create_category(
        category: CategoryCreate,
        session: AsyncSession = Depends(get_async_session),
        current_user: User = Depends(get_current_user),
):
    return await category_service.create_category(category, current_user.id, session)


@category_router.get("/{id}", response_model=CategoryResponse)
async def get_category(
        id: int,
        session: AsyncSession = Depends(get_async_session),
        current_user: User = Depends(get_current_user),
):
    try:
        return await category_service.get_category_by_id(id, current_user.id, session)
    except CategoryNotFoundException as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))


@category_router.patch("/{id}", response_model=CategoryResponse)
async def update_category(
        id: int,
        data: CategoryUpdate,
        session: AsyncSession = Depends(get_async_session),
        current_user: User = Depends(get_current_user),
):
    try:
        return await category_service.update_category(id, data, current_user.id, session)
    except CategoryNotFoundException as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except SystemCategoryModificationException as e:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=str(e))


@category_router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_category(
        id: int,
        session: AsyncSession = Depends(get_async_session),
        current_user: User = Depends(get_current_user),
):
    try:
        await category_service.delete_category(id, current_user.id, session)
    except CategoryNotFoundException as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except SystemCategoryModificationException as e:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=str(e))
    except CategoryInUseException as e:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(e))
