from uuid import UUID, uuid4
from http import HTTPStatus

import pytest
from unittest.mock import patch
from fastapi import HTTPException
from sqlalchemy.exc import IntegrityError, SQLAlchemyError

from src.api.validators import (
    check_task_exists_by_uuid,
    completed_task_can_not_be_update,
)
from src.models.task import StatusEnum, Task
from src.crud.task import TaskCRUD
from src.schemas.task import TaskCreate


CREATE_DATA = {'title': 'Test Task', 'description': 'Desc', 'status': 'created'}


@pytest.mark.asyncio
async def test_create_task(async_client):
    response = await async_client.post('/tasks', json=CREATE_DATA)
    assert response.status_code == HTTPStatus.CREATED
    json_data = response.json()
    assert json_data['title'] == 'Test Task'
    assert UUID(json_data['uuid'])


@pytest.mark.asyncio
async def test_get_all_task(async_client):
    for _ in range(3):
        await async_client.post('/tasks', json=CREATE_DATA)
    response = await async_client.get('/tasks')
    assert response.status_code == HTTPStatus.OK
    assert len(response.json()) == 3


@pytest.mark.asyncio
async def test_get_task(async_client):
    create_resp = await async_client.post('/tasks', json=CREATE_DATA)
    task_uuid = create_resp.json()['uuid']
    response = await async_client.get(f'/tasks/{task_uuid}')
    assert response.status_code == HTTPStatus.OK
    task = response.json()
    assert task['title'] == CREATE_DATA['title']
    assert task['description'] == CREATE_DATA['description']
    assert task['status'] == CREATE_DATA['status']


@pytest.mark.asyncio
async def test_get_by_not_correct_uuid(async_client):
    response = await async_client.get(f'/tasks/{1}')
    assert response.status_code == 422


@pytest.mark.asyncio
async def test_get_not_existen_task(async_client):
    response = await async_client.get(f'/tasks/{uuid4()}')
    assert response.status_code == HTTPStatus.BAD_REQUEST


@pytest.mark.asyncio
async def test_patch_task(async_client):
    resp = await async_client.post('/tasks', json=CREATE_DATA)
    task_uuid = resp.json()['uuid']
    update_data = {'title': 'Updated Task'}
    response = await async_client.patch(
        f'/tasks/{task_uuid}',
        json=update_data,
    )
    assert response.status_code == HTTPStatus.OK
    assert response.json()['title'] == 'Updated Task'


@pytest.mark.asyncio
async def test_delete_task(async_client):
    resp = await async_client.post('/tasks', json=CREATE_DATA)
    task_uuid = resp.json()['uuid']
    response = await async_client.delete(f'/tasks/{task_uuid}')
    assert response.status_code == 204
    get_resp = await async_client.get(f'/tasks/{task_uuid}')
    assert get_resp.status_code == HTTPStatus.BAD_REQUEST


@pytest.mark.asyncio
async def test_check_task_exists_by_uuid_raises(session):
    fake_uuid = uuid4()
    with pytest.raises(HTTPException) as exc:
        await check_task_exists_by_uuid(fake_uuid, session)
    assert exc.value.status_code == HTTPStatus.BAD_REQUEST


@pytest.mark.asyncio
async def test_completed_task_can_not_be_update(session):
    task = Task(title='Done Task', status=StatusEnum.COMPLETED.value)
    session.add(task)
    await session.commit()
    await session.refresh(task)
    with pytest.raises(HTTPException) as exc:
        await completed_task_can_not_be_update(task, session)
    assert exc.value.status_code == HTTPStatus.BAD_REQUEST


@pytest.mark.asyncio
async def test_create_integrity_error(session):
    crud = TaskCRUD(Task)
    schema = TaskCreate(**CREATE_DATA)
    with patch.object(
        session,
        'add',
        side_effect=IntegrityError('msg', params=None, orig=None),
    ):
        with pytest.raises(HTTPException) as exc:
            await crud.create(schema, session)
        assert exc.value.status_code == HTTPStatus.BAD_REQUEST
        assert 'Create data error' in exc.value.detail


@pytest.mark.asyncio
async def test_create_sqlalchemy_error(session):
    crud = TaskCRUD(Task)
    schema = TaskCreate(**CREATE_DATA)
    with patch.object(
        session,
        'commit',
        side_effect=SQLAlchemyError('some error'),
    ):
        with pytest.raises(HTTPException) as exc:
            await crud.create(schema, session)
        assert exc.value.status_code == HTTPStatus.BAD_REQUEST
        assert 'Server error' in exc.value.detail


@pytest.mark.asyncio
async def test_check_task_exists_by_uuid_validator(async_client, session):
    response = await async_client.post('/tasks', json=CREATE_DATA)
    assert response.status_code == HTTPStatus.CREATED
    new_task = response.json()
    new_task_after_validation = await check_task_exists_by_uuid(
        UUID(new_task['uuid']), session
    )
    assert new_task['uuid'] == str(new_task_after_validation.uuid)
    assert new_task['title'] == new_task_after_validation.title
    assert new_task['description'] == new_task_after_validation.description
    assert new_task['status'] == new_task_after_validation.status
