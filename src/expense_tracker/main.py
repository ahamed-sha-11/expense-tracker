from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

import fastapi
import uvicorn
from redis.asyncio import Redis

from expense_tracker.core.config import REDIS_URL
from expense_tracker.core.database import async_session, create_db_and_tables, engine
from expense_tracker.routers.category import category_router
from expense_tracker.routers.transaction import transaction_router
from expense_tracker.routers.user import user_router
from expense_tracker.services import category_service


@asynccontextmanager
async def lifespan(app: fastapi.FastAPI) -> AsyncIterator[None]:
    await create_db_and_tables()
    async with async_session() as session:
        await category_service.ensure_default_category(session)

    app.state.redis = Redis.from_url(REDIS_URL, decode_responses=True)

    yield

    await app.state.redis.aclose()
    await engine.dispose()

app = fastapi.FastAPI(lifespan=lifespan)
app.include_router(transaction_router)
app.include_router(category_router)
app.include_router(user_router)


def main():
    uvicorn.run("expense_tracker.main:app", reload=True, host="127.0.0.1", port=8080)


if __name__ == "__main__":
    main()