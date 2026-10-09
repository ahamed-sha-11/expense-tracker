from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

import fastapi

from .db import create_db_and_tables, engine
from .transactions.transaction_router import transaction_router


@asynccontextmanager
async def lifespan(app: fastapi.FastAPI) -> AsyncIterator[None]:
    await create_db_and_tables()
    yield
    await engine.dispose()


app = fastapi.FastAPI(lifespan=lifespan)

@app.get("/")
async def root():
    return {"message": "Hello World"}


app.include_router(transaction_router)
