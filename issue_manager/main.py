from fastapi import FastAPI

from issue_manager.core.config import settings
from issue_manager.api.routers import main_router


app = FastAPI(
    title=settings.fastapi_title,
    description=settings.fastapi_description
)
app.router.include_router(main_router)
