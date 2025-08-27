import datetime

from sqlalchemy.orm import mapped_column, Mapped, declared_attr, DeclarativeBase
from sqlalchemy.ext.asyncio import AsyncAttrs


class BaseModel(AsyncAttrs, DeclarativeBase):
    __abctract__ = True

    @declared_attr
    def __tablename__(cls) -> str:
        return cls.__name__.lower()
