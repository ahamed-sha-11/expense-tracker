from fastapi import APIRouter, status, Depends

from expense_tracker.db import get_async_session
from expense_tracker.transactions.schemas import TransactionCreate

transaction_router = APIRouter(
    prefix="/transactions",
    tags=["transactions"],
)



@transaction_router.get("/")
async def get_all_transactions(page: int = 1, size: int = 100):
    pass

@transaction_router.post(
    "/",
    status_code=status.HTTP_201_CREATED
)
async def create_transaction(transaction:TransactionCreate, session = Depends(get_async_session)):
    pass

@transaction_router.get("/{id}")
async def get_transaction(id: int):
    pass

@transaction_router.patch("/{id}")
async def update_transaction(id: int):
    pass

@transaction_router.delete("/{id}")
async def delete_transaction(id: int):
    pass