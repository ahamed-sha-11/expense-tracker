
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.ext.asyncio import AsyncSession

from expense_tracker.core.database import get_async_session
from expense_tracker.core.security import get_current_user
from expense_tracker.exceptions.category import CategoryNotFoundException
from expense_tracker.exceptions.transaction import NegativeTransactionException, TransactionNotFoundException
from expense_tracker.models.user import User
from expense_tracker.schemas.transaction import TransactionCreate, TransactionResponse, TransactionUpdate
from expense_tracker.services import transaction_service

transaction_router = APIRouter(
    prefix="/transactions",
    tags=["transactions"],
)


@transaction_router.get("/", response_model=list[TransactionResponse])
async def get_all_transactions(
    page: int = Query(1, ge=1),
    size: int = Query(100, ge=1, le=100),
    session: AsyncSession = Depends(get_async_session),
    current_user: User = Depends(get_current_user),
):
    return await transaction_service.get_all_transactions(current_user.id, session, page, size)

@transaction_router.get("/{id}", response_model=TransactionResponse)
async def get_transaction(
    id : int,
    session: AsyncSession = Depends(get_async_session),
    current_user: User = Depends(get_current_user),
):
    try:
        return await transaction_service.get_transaction_by_id(id, current_user.id, session)
    except TransactionNotFoundException  as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

@transaction_router.post("/", response_model=TransactionResponse, status_code=status.HTTP_201_CREATED)
async def create_transaction(
    transaction: TransactionCreate,
    session: AsyncSession = Depends(get_async_session),
    current_user: User = Depends(get_current_user),
):
    try:
        return await transaction_service.create_transaction(transaction, current_user.id, session)
    except NegativeTransactionException as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except CategoryNotFoundException as e:
        raise HTTPException( status_code=status.HTTP_422_UNPROCESSABLE_CONTENT, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

@transaction_router.patch("/{transaction_id}", response_model=TransactionResponse)
async def update_transaction(
    transaction_id: int,
    data: TransactionUpdate,
    session: AsyncSession = Depends(get_async_session),
    current_user: User = Depends(get_current_user),
):
    try:
        return await transaction_service.update_transaction(transaction_id, data, current_user.id, session)
    except TransactionNotFoundException as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except CategoryNotFoundException as e:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_CONTENT, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


@transaction_router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_transaction(
    id: int,
    session: AsyncSession = Depends(get_async_session),
    current_user: User = Depends(get_current_user),
):
    try:
        await transaction_service.delete_transaction(id, current_user.id, session)
    except TransactionNotFoundException as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
