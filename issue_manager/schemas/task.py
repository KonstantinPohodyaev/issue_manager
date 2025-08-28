from typing import Optional

from pydantic import BaseModel, Field
from src.database.enums import StatusEnum


class BaseTask(BaseModel):
    uuid: Optional[str] = Field(None)
    title: Optional[str] = Field(None, min_length=1, max_length=128)
    description: Optional[str] = Field(None)
    status: 