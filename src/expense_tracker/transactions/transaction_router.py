
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from expense_tracker.db import get_async_session
from expense_tracker.transactions import transaction_service
from expense_tracker.transactions.exceptions import CategoryNotFoundException, NegativeTransactionException
from expense_tracker.transactions.schemas import TransactionCreate, TransactionResponse

transaction_router = APIRouter(
    prefix="/transactions",
    tags=["transactions"],
)


@transaction_router.get("/")
async def get_all_transactions(page: int = 1, size: int = 100):
    pass


@transaction_router.post(
    "/",
    response_model=TransactionResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_transaction(transaction: TransactionCreate, session: AsyncSession = Depends(get_async_session)):
    try:
        return await transaction_service.create_transaction(transaction, session)
    except NegativeTransactionException as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except CategoryNotFoundException as e:
        raise HTTPException( status_code=status.HTTP_422_UNPROCESSABLE_CONTENT, detail=str(e))

@transaction_router.get("/{id}")
async def get_transaction(id: int):
    pass


@transaction_router.patch("/{id}")
async def update_transaction(id: int):
    pass


@transaction_router.delete("/{id}")
async def delete_transaction(id: int):
    pass