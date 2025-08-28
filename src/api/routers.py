from fastapi import APIRouter

from src.api.v1.endpoints import task_router

main_router = APIRouter()
main_router.include_router(task_router, prefix='/tasks', tags=['tasks'])
