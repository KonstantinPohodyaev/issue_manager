from fastapi import FastAPI

from src.api.routers import main_router
from src.core.config import settings

app = FastAPI(
    title=settings.fastapi_title,
    description=settings.fastapi_description
)
app.router.include_router(main_router)
