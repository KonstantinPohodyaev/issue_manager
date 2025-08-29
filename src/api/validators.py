from uuid import UUID

from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from src.models.task import Task
from src.crud.task import task_crud
from src.database.enums import StatusEnum


async def check_task_exists_by_uuid(
    task_uuid: UUID,
    session: AsyncSession
) -> None:
    task = await task_crud.get(task_uuid, session)
    if not task:
        raise HTTPException(
            detail=f'Task instance with uuid = {task_uuid} does not exist!',
            status_code=status.HTTP_400_BAD_REQUEST
        )
    return task


async def completed_task_can_not_be_update(
    task: Task,
    session: AsyncSession
) -> None:
    if task.status == StatusEnum.COMPLETED.value:
        raise HTTPException(
            detail=f'Task `{task.title}` has been already comleted!',
            status_code=status.HTTP_400_BAD_REQUEST
        )
