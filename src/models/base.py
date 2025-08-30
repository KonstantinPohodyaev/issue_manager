from sqlalchemy.ext.asyncio import AsyncAttrs
from sqlalchemy.orm import DeclarativeBase, declared_attr


class BaseModel(AsyncAttrs, DeclarativeBase):
    """
    Base class for all database models.

    Inherits asynchronous attributes from AsyncAttrs and base ORM
    functionality from DeclarativeBase.
    """

    __abstract__ = True

    @declared_attr
    def __tablename__(cls) -> str:
        """
        Generate table name automatically based on class name.

        Returns:
            str: Lowercase name of the class as table name.
        """
        return cls.__name__.lower()
