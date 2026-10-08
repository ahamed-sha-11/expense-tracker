import fastapi
from fastapi import APIRouter
from .transaction import transaction_router
app = fastapi.FastAPI()

@app.get("/")
async def root():
    return {"message": "Hello World"}


app.include_router(transaction_router)