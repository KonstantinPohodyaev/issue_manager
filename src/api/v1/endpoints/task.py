from fastapi import APIRouter, status, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.schemas.task import TaskRead
from src.database.db import get_async_session
from src.crud.task import task_crud


router = APIRouter()


@router.get(
    '',
    status_code=status.HTTP_200_OK,
    response_model=list[TaskRead],
    response_model_exclude_none=True
)
async def get_all_tasks(
    session: AsyncSession = Depends(get_async_session)
):
    return await task_crud.get_all(session)
