from sqlalchemy.ext.asyncio import AsyncAttrs
from sqlalchemy.orm import DeclarativeBase, declared_attr


class BaseModel(AsyncAttrs, DeclarativeBase):
    __abctract__ = True

    @declared_attr
    def __tablename__(cls) -> str:
        return cls.__name__.lower()
