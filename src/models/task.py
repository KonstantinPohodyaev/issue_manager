from uuid import UUID

from sqlalchemy.orm import Mapped, mapped_column

from src.models.base import BaseModel
from src.database.enums import StatusEnum


class Task(BaseModel):
    uuid: Mapped[UUID] = mapped_column(
        primary_key=True, unique=True
    )
    title: Mapped[str] = mapped_column(
        nullable=False
    )
    description: Mapped[str] = mapped_column(
        nullable=True
    )
    status: Mapped[StatusEnum] = mapped_column(
        nullable=False
    )
