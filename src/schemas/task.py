from typing import Optional
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field

from src.database.enums import StatusEnum


TITLE_MIN_LENGTH = 1
TITLE_MAX_LENGTH = 128

TASK_CREATE_JSON_EXAMPLES = {
    'correct_request': {
        'summary': 'Correct request',
        'description': 'All attrs are correct',
        'value': {
            'title': 'title',
            'description': 'description',
            'status': 'created'
        }
    },
    'without_desc': {
        'summary': 'Correct request without description',
        'description': 'Description field is empty',
        'value': {
            'title': 'title',
            'status': 'created'
        }
    },
    'empty_title': {
        'summary': 'Empty title',
        'description': 'Title field is empty',
        'value': {
            'description': 'description',
            'status': 'created'
        }
    },
    'status_not_from_enum': {
        'summary': 'Status is not registrated value',
        'description': 'Status field has not registrated value',
        'value': {
            'title': 'title',
            'description': 'description',
            'status': 'HAPPY STATUS'
        }
    },
}


class BaseTask(BaseModel):
    title: Optional[str] = Field(
        None,
        min_length=TITLE_MIN_LENGTH,
        max_length=TITLE_MAX_LENGTH,
        description=(
            f'Name of task (from {TITLE_MIN_LENGTH} to {TITLE_MAX_LENGTH})'
            f'symbols.'
        )
    )
    description: Optional[str] = Field(
        None,
        description='Description of task.'
    )
    status: Optional[StatusEnum] = Field(
        None,
        description='Task`s status.'
    )

    model_config = ConfigDict(
        title='Base schema for Task model.'
    )


class TaskRead(BaseTask):
    uuid: Optional[UUID] = Field(None)

    model_config = ConfigDict(
        title='Task DB schema',
        from_attributes=True
    )


class TaskCreate(BaseModel):
    title: str = Field(..., min_length=1, max_length=128)
    description: Optional[str] = Field(None)
    status: StatusEnum
    model_config = ConfigDict(
        title='Task create schema',
    )


class TaskUpdate(BaseTask):
    model_config = ConfigDict(
        title='Task update schema'
    )
