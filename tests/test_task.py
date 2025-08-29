import pytest
from uuid import UUID, uuid4
from fastapi import HTTPException
from src.api.validators import (
    check_task_exists_by_uuid,
    completed_task_can_not_be_update,
)
from src.models.task import Task, StatusEnum


@pytest.mark.asyncio
async def test_create_task(async_client):
    data = {'title': 'Test Task', 'description': 'Desc', 'status': 'created'}
    response = await async_client.post('/tasks', json=data)
    assert response.status_code == 201
    json_data = response.json()
    assert json_data['title'] == 'Test Task'
    assert UUID(json_data['uuid'])

@pytest.mark.asyncio
async def test_get_task(async_client):
    data = {'title': 'Get Task', 'description': '', 'status': 'created'}
    create_resp = await async_client.post('/tasks', json=data)
    task_uuid = create_resp.json()['uuid']
    response = await async_client.get(f'/tasks/{task_uuid}')
    assert response.status_code == 200
    assert response.json()['title'] == 'Get Task'

@pytest.mark.asyncio
async def test_patch_task(async_client):
    data = {'title': 'Patch Task', 'description': '', 'status': 'created'}
    resp = await async_client.post('/tasks', json=data)
    task_uuid = resp.json()['uuid']
    update_data = {'title': 'Updated Task'}
    response = await async_client.patch(f'/tasks/{task_uuid}', json=update_data)
    assert response.status_code == 200
    assert response.json()['title'] == 'Updated Task'

@pytest.mark.asyncio
async def test_delete_task(async_client):
    data = {'title': 'Delete Task', 'description': '', 'status': 'created'}
    resp = await async_client.post('/tasks', json=data)
    task_uuid = resp.json()['uuid']
    response = await async_client.delete(f'/tasks/{task_uuid}')
    assert response.status_code == 204
    get_resp = await async_client.get(f'/tasks/{task_uuid}')
    assert get_resp.status_code == 400

@pytest.mark.asyncio
async def test_check_task_exists_by_uuid_raises(session):
    fake_uuid = uuid4()
    with pytest.raises(HTTPException) as exc:
        await check_task_exists_by_uuid(fake_uuid, session)
    assert exc.value.status_code == 400

@pytest.mark.asyncio
async def test_completed_task_can_not_be_update(session):
    task = Task(title='Done Task', status=StatusEnum.COMPLETED.value)
    session.add(task)
    await session.commit()
    await session.refresh(task)
    with pytest.raises(HTTPException) as exc:
        await completed_task_can_not_be_update(task, session)
    assert exc.value.status_code == 400
