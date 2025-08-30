from uuid import UUID

from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from src.crud.task import task_crud
from src.database.enums import StatusEnum
from src.models.task import Task


async def check_task_exists_by_uuid(
    task_uuid: UUID,
    session: AsyncSession
) -> Task:
    """
    Check if a task exists by its UUID.

    Args:
        task_uuid (UUID): Unique identifier of the task.
        session (AsyncSession): SQLAlchemy asynchronous session.

    Raises:
        HTTPException: If the task with given UUID does not exist (status 400).

    Returns:
        Task: The task instance from the database.
    """
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
    """
    Raise an exception if a task is already completed.

    Args:
        task (Task): Task instance to check.
        session (AsyncSession): SQLAlchemy asynchronous session.

    Raises:
        HTTPException: If the task status is 'COMPLETED' (status 400).
    """
    if task.status == StatusEnum.COMPLETED.value:
        raise HTTPException(
            detail=f'Task `{task.title}` has been already completed!',
            status_code=status.HTTP_400_BAD_REQUEST
        )
