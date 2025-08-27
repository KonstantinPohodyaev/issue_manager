from typing import Any, AsyncGenerator

from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

from issue_manager.core.config import settings


if settings.DEBUG:
    DB_URL = settings.test_db_url
else:
    DB_URL = settings.get_db_url


engine = create_async_engine(DB_URL)
AsyncSessionLocal = sessionmaker(
    engine, class_=AsyncSession, expire_on_commit=False
)

async def get_async_session() -> AsyncGenerator[AsyncSession, Any]:
    async with AsyncSessionLocal() as async_session:
        yield async_session
