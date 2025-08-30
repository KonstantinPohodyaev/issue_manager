"""
Test configuration for Issue Manager API.

Provides asynchronous fixtures for:
- HTTP client
- Database session
- Database setup/teardown for each test
"""

import pytest_asyncio
from httpx import AsyncClient
from httpx._transports.asgi import ASGITransport
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

from src.main import app
from src.models.base import BaseModel
from src.core.config import settings

# Asynchronous test database engine
test_engine = create_async_engine(
    settings.get_db_url, echo=True
)

# Session factory for test DB
TestAsyncSessionLocal = sessionmaker(
    test_engine, expire_on_commit=False, class_=AsyncSession
)


@pytest_asyncio.fixture(scope='function')
async def async_client():
    """
    Provides an Async HTTP client for FastAPI testing.

    Uses ASGITransport to avoid running an external server.
    """
    async with AsyncClient(
        transport=ASGITransport(app=app),
        base_url='http://testserver',
    ) as client:
        yield client


@pytest_asyncio.fixture(scope='function')
async def session():
    """
    Provides a SQLAlchemy AsyncSession for tests.

    Rolls back any changes after the test to ensure isolation.
    """
    async with TestAsyncSessionLocal() as session:
        yield session
        await session.rollback()


@pytest_asyncio.fixture(scope='function', autouse=True)
async def setup_db():
    """
    Creates all tables before each test and drops them after.

    Ensures each test runs with a clean database.
    """
    async with test_engine.begin() as conn:
        await conn.run_sync(BaseModel.metadata.create_all)
    yield
    async with test_engine.begin() as conn:
        await conn.run_sync(BaseModel.metadata.drop_all)
