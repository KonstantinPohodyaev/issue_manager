import pytest_asyncio
from httpx import AsyncClient
from httpx._transports.asgi import ASGITransport
from src.main import app
from src.database.db import AsyncSessionLocal, engine
from src.models.base import BaseModel

@pytest_asyncio.fixture(scope='function')
async def async_client():
    async with AsyncClient(transport=ASGITransport(app=app), base_url='http://test') as client:
        yield client

@pytest_asyncio.fixture(scope='function')
async def session():
    async with AsyncSessionLocal() as session:
        yield session
        await session.rollback()

@pytest_asyncio.fixture(scope='function', autouse=True)
async def setup_db():
    async with engine.begin() as conn:
        await conn.run_sync(BaseModel.metadata.create_all)
    yield
    async with engine.begin() as conn:
        await conn.run_sync(BaseModel.metadata.drop_all)
