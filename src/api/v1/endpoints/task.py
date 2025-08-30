from uuid import UUID

from fastapi import APIRouter, Body, Depends, status, Path
from sqlalchemy.ext.asyncio import AsyncSession

from src.api.validators import (
    check_task_exists_by_uuid,
    completed_task_can_not_be_update,
)
from src.crud.task import task_crud
from src.database.db import get_async_session
from src.schemas.task import (
    TaskCreate,
    TaskRead,
    TaskUpdate,
    TASK_CREATE_JSON_EXAMPLES,
)


router = APIRouter()

UUID_PATH_DESCRIPTION = 'Unique identifier of task instance'


@router.get(
    '',
    status_code=status.HTTP_200_OK,
    response_model=list[TaskRead],
    response_model_exclude_none=True,
    summary='Get all tasks'
)
async def get_all_tasks(
    session: AsyncSession = Depends(get_async_session)
):
    """
    Retrieve all tasks from the database.

    - **uuid**: unique identifier of the task  
    - **title**: short title of the task  
    - **description**: optional description  
    - **status**: current status (`created`, `in_progress`, `done`)
    """
    return await task_crud.get_all(session)


@router.get(
    '/{task_uuid}',
    status_code=status.HTTP_200_OK,
    response_model=TaskRead,
    response_model_exclude_none=True,
    summary='Get tasks by unique uuid',
)
async def get_task_by_id(
    task_uuid: UUID = Path(..., description=UUID_PATH_DESCRIPTION),
    session: AsyncSession = Depends(get_async_session),
):
    """
    Retrieve a single task by its unique UUID.

    - **task_uuid**: unique identifier of the task  
    Returns task details if it exists, otherwise raises a 404 error.
    """
    await check_task_exists_by_uuid(task_uuid, session)
    return await task_crud.get(task_uuid, session)


@router.post(
    '',
    status_code=status.HTTP_201_CREATED,
    response_model=TaskRead,
    response_model_exclude_none=True,
    summary='Create new task',
)
async def create_task(
    create_schema: TaskCreate = Body(
        ...,
        openapi_examples=TASK_CREATE_JSON_EXAMPLES
    ),
    session: AsyncSession = Depends(get_async_session),
):
    """
    Create a new task.

    - **title**: short title of the task (required)  
    - **description**: optional description  
    - **status**: initial status (`created` by default)  
    """
    return await task_crud.create(create_schema, session)


@router.patch(
    '/{task_uuid}',
    status_code=status.HTTP_200_OK,
    response_model=TaskRead,
    response_model_exclude_none=True,
    summary='Partial update of existen task',
)
async def update_task(
    update_schema: TaskUpdate,
    task_uuid: UUID = Path(..., description=UUID_PATH_DESCRIPTION),
    session: AsyncSession = Depends(get_async_session)
):
    """
    Partially update an existing task.

    - **task_uuid**: unique identifier of the task  
    - **update_schema**: fields to update  
    Completed tasks cannot be updated.
    """
    task = await check_task_exists_by_uuid(task_uuid, session)
    await completed_task_can_not_be_update(task, session)
    return await task_crud.update(
        task,
        update_schema,
        session,
    )


@router.delete(
    '/{task_uuid}',
    status_code=status.HTTP_204_NO_CONTENT,
    summary='Delete task',
)
async def delete_task(
    task_uuid: UUID = Path(..., description=UUID_PATH_DESCRIPTION),
    session: AsyncSession = Depends(get_async_session),
):
    """
    Delete a task by its unique UUID.

    - **task_uuid**: unique identifier of the task  
    Removes the task from the database if it exists, otherwise raises a 404 error.
    """
    await check_task_exists_by_uuid(task_uuid, session)
    return await task_crud.delete(
        await task_crud.get(task_uuid, session),
        session,
    )
