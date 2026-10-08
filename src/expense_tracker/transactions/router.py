from fastapi import APIRouter

transaction_router = APIRouter(
    prefix="/transactions",
    tags=["transactions"],
)



@transaction_router.get("/")
async def get_all_transactions(page: int = 1, size: int = 100):
    pass

@transaction_router.post("/")
async def create_transaction():
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