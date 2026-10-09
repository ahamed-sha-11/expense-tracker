from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from expense_tracker.db import get_async_session
from expense_tracker.categories import category_service
from expense_tracker.categories.exceptions import CategoryNotFoundException
from expense_tracker.categories.schemas import CategoryCreate, CategoryResponse

category_router = APIRouter(
    prefix="/categories",
    tags=["categories"],
)


@category_router.get("/")
async def get_all_categories():
    pass


@category_router.post("/", response_model=CategoryResponse,status_code=status.HTTP_201_CREATED)
async def create_category(category: CategoryCreate, session: AsyncSession = Depends(get_async_session)):
    return await category_service.create_category(category, session)


@category_router.get("/{id}",response_model=CategoryResponse)
async def get_category(id: int, session: AsyncSession = Depends(get_async_session)):
    try:
        return await category_service.get_category_by_id(id, session)
    except CategoryNotFoundException as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))


@category_router.patch("/{id}")
async def update_category(id: int):
    pass


@category_router.delete("/{id}")
async def delete_category(id: int):
    pass
