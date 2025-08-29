from typing import Optional
from uuid import UUID

from pydantic import BaseModel, Field, ConfigDict
from src.database.enums import StatusEnum


class BaseTask(BaseModel):
    title: Optional[str] = Field(None, min_length=1, max_length=128)
    description: Optional[str] = Field(None)
    status: Optional[StatusEnum] = Field(None)


class TaskRead(BaseTask):
    uuid: Optional[UUID] = Field(None)

    model_config = ConfigDict(
        title='Display schema in responces',
        from_attributes=True
    )


class TaskCreate(BaseModel):
    title: str = Field(..., min_length=1, max_length=128)
    description: Optional[str] = Field(None)
    status: StatusEnum


class TaskUpdate(BaseTask):
    pass
