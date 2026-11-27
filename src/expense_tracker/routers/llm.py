from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.ext.asyncio import AsyncSession

llm_router = APIRouter(
    prefix="/llm",
    tags=["llm"],
)

@llm_router.post("/credentials")
async def save_llm_credentials():
    pass
