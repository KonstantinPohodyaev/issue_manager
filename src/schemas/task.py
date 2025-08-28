from typing import Optional

from pydantic import BaseModel, Field, ConfigDict
from src.database.enums import StatusEnum


class BaseTask(BaseModel):
    uuid: Optional[str] = Field(None)
    title: Optional[str] = Field(None, min_length=1, max_length=128)
    description: Optional[str] = Field(None)
    status: Optional[StatusEnum] = Field(None)


class TaskRead(BaseTask):
    pass

    model_config = ConfigDict(
        title='Display schema in responces',
        from_attributes=True
    )


class TaskCreate(BaseModel):
    uuid: str = Field(...)
    title: str = Field(..., min_length=1, max_length=128)
    description: Optional[str] = Field(None)
    status: StatusEnum = Field(...)


class TaskUpdate(BaseTask):
    pass
