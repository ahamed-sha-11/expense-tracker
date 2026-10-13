from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

import fastapi

from .categories import category_service
from .categories.category_router import category_router
from .db import create_db_and_tables, engine, async_session
from .transactions.transaction_router import transaction_router
from .users.user_router import user_router


@asynccontextmanager
async def lifespan(app: fastapi.FastAPI) -> AsyncIterator[None]:
    await create_db_and_tables()
    async with async_session() as session:
        await category_service.ensure_default_category(session)
    yield
    await engine.dispose()


app = fastapi.FastAPI(lifespan=lifespan)
app.include_router(transaction_router)
app.include_router(category_router)
app.include_router(user_router)