from typing import Optional
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field

from src.database.enums import StatusEnum

TITLE_MIN_LENGTH = 1
TITLE_MAX_LENGTH = 128

TASK_CREATE_JSON_EXAMPLES = {
    'correct_request': {
        'summary': 'Correct request',
        'description': 'All attributes are correct',
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
        'summary': 'Status is not registered value',
        'description': 'Status field has an invalid value',
        'value': {
            'title': 'title',
            'description': 'description',
            'status': 'HAPPY STATUS'
        }
    },
}


class BaseTask(BaseModel):
    """
    Base schema for Task model.

    Fields:
        title (str | None): Name of task, 1-128 symbols.
        description (str | None): Optional description of task.
        status (StatusEnum | None): Current task status.
    """
    title: Optional[str] = Field(
        None,
        min_length=TITLE_MIN_LENGTH,
        max_length=TITLE_MAX_LENGTH,
        description=(
            f'Name of task (from {TITLE_MIN_LENGTH} to '
            f'{TITLE_MAX_LENGTH} symbols).'
        )
    )
    description: Optional[str] = Field(
        None,
        description='Description of task.'
    )
    status: Optional[StatusEnum] = Field(
        None,
        description="Task's status."
    )

    model_config = ConfigDict(
        title='Base schema for Task model.'
    )


class TaskRead(BaseTask):
    """
    Schema for reading a Task from the DB.

    Fields:
        uuid (UUID | None): Unique identifier of the task.
    """
    uuid: Optional[UUID] = Field(None)

    model_config = ConfigDict(
        title='Task DB schema',
        from_attributes=True
    )


class TaskCreate(BaseModel):
    """
    Schema for creating a new Task.

    Fields:
        title (str): Title of the task (required).
        description (str | None): Optional description.
        status (StatusEnum): Task status (required).
    """
    title: str = Field(..., min_length=1, max_length=128)
    description: Optional[str] = Field(None)
    status: StatusEnum

    model_config = ConfigDict(
        title='Task create schema',
    )


class TaskUpdate(BaseTask):
    """
    Schema for updating a Task.

    All fields are optional; only provided fields will be updated.
    """
    model_config = ConfigDict(
        title='Task update schema'
    )
