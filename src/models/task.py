from uuid import UUID, uuid4
from sqlalchemy.orm import Mapped, mapped_column

from src.database.enums import StatusEnum
from src.models.base import BaseModel


class Task(BaseModel):
    """
    Task model for issue management.

    Attributes:
        uuid (UUID): Unique identifier of the task, primary key.
        title (str): Title of the task, required.
        description (str | None): Optional description of the task.
        status (StatusEnum): Current status of the task.
    """

    uuid: Mapped[UUID] = mapped_column(
        primary_key=True,
        default=uuid4,
    )
    title: Mapped[str] = mapped_column(
        nullable=False,
    )
    description: Mapped[str] = mapped_column(
        nullable=True,
    )
    status: Mapped[StatusEnum] = mapped_column(
        nullable=False,
    )
