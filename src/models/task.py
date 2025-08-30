from uuid import UUID, uuid4

from sqlalchemy.orm import Mapped, mapped_column

from src.database.enums import StatusEnum
from src.models.base import BaseModel


class Task(BaseModel):
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
