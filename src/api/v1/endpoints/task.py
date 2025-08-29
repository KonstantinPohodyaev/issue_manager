from uuid import UUID

from fastapi import APIRouter, status, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.schemas.task import TaskRead, TaskCreate, TaskUpdate
from src.database.db import get_async_session
from src.api.validators import (
    check_task_exists_by_uuid,
    completed_task_can_not_be_update,
)
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


@router.get(
    '/{task_uuid}',
    status_code=status.HTTP_200_OK,
    response_model=TaskRead,
    response_model_exclude_none=True
)
async def get_task_by_id(
    task_uuid: UUID,
    session: AsyncSession = Depends(get_async_session),
):
    await check_task_exists_by_uuid(task_uuid, session)
    return await task_crud.get(task_uuid, session)

@router.post(
    '',
    status_code=status.HTTP_201_CREATED,
    response_model=TaskRead,
    response_model_exclude_none=True
)
async def get_task_by_id(
    create_schema: TaskCreate,
    session: AsyncSession = Depends(get_async_session),
):
    return await task_crud.create(create_schema, session)


@router.patch(
    '/{task_uuid}',
    status_code=status.HTTP_200_OK,
    response_model=TaskRead,
    response_model_exclude_none=True
)
async def update_task(
    task_uuid: UUID,
    update_schema: TaskUpdate,
    session: AsyncSession = Depends(get_async_session)
):
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
)
async def delete_task(
    task_uuid: UUID,
    session: AsyncSession = Depends(get_async_session),
):
    await check_task_exists_by_uuid(task_uuid, session)
    return await task_crud.delete(
        await task_crud.get(task_uuid, session),
        session
    )
