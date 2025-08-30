from uuid import UUID

from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession


class BaseCRUD:
    """
    Base class for CRUD operations on SQLAlchemy models.

    Attributes:
        model: SQLAlchemy model class.
    """

    def __init__(self, model):
        self.model = model

    async def get_all(self, session: AsyncSession):
        """
        Retrieve all records of the model from the database.

        Args:
            session (AsyncSession): Async SQLAlchemy session.

        Returns:
            List[model]: List of model instances.
        """
        return (
            await session.execute(
                select(self.model)
            )
        ).scalars().all()

    async def get(
        self,
        uuid: UUID,
        session: AsyncSession,
    ):
        """
        Retrieve a single record by UUID.

        Args:
            uuid (UUID): Unique identifier of the record.
            session (AsyncSession): Async SQLAlchemy session.

        Returns:
            model | None: Model instance if found, else None.
        """
        return (
            await session.execute(
                select(self.model).where(self.model.uuid == uuid)
            )
        ).scalar()

    async def create(
        self,
        create_schema,
        session: AsyncSession,
        commit_on: bool = True,
    ):
        """
        Create a new record in the database.

        Args:
            create_schema: Pydantic schema for creating the record.
            session (AsyncSession): Async SQLAlchemy session.
            commit_on (bool): Commit after creation if True.

        Raises:
            HTTPException: If IntegrityError or SQLAlchemyError occurs.

        Returns:
            model: Created model instance.
        """
        new_task = self.model(**create_schema.model_dump())
        try:
            session.add(new_task)
            if commit_on:
                await session.commit()
                await session.refresh(new_task)
            return new_task
        except IntegrityError as error:
            await session.rollback()
            raise HTTPException(
                detail=f'Create data error: {str(error)}',
                status_code=status.HTTP_400_BAD_REQUEST
            )
        except SQLAlchemyError as error:
            await session.rollback()
            raise HTTPException(
                detail=f'Server error: {str(error)}',
                status_code=status.HTTP_400_BAD_REQUEST
            )

    async def update(
        self,
        task,
        update_schema,
        session: AsyncSession,
        commit_on: bool = True
    ):
        """
        Update an existing record with new data.

        Args:
            task: Model instance to update.
            update_schema: Pydantic schema with updated fields.
            session (AsyncSession): Async SQLAlchemy session.
            commit_on (bool): Commit after update if True.

        Raises:
            HTTPException: If IntegrityError or SQLAlchemyError occurs.

        Returns:
            model: Updated model instance.
        """
        update_data = update_schema.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(task, field, value)
        try:
            session.add(task)
            if commit_on:
                await session.commit()
                await session.refresh(task)
            return task
        except IntegrityError as error:
            await session.rollback()
            raise HTTPException(
                detail=f'Update data error: {str(error)}',
                status_code=status.HTTP_400_BAD_REQUEST,
            )
        except SQLAlchemyError as error:
            await session.rollback()
            raise HTTPException(
                detail=f'Server error: {str(error)}',
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

    async def delete(
        self,
        task,
        session: AsyncSession,
        commit_on: bool = True
    ):
        """
        Delete a record from the database.

        Args:
            task: Model instance to delete.
            session (AsyncSession): Async SQLAlchemy session.
            commit_on (bool): Commit after deletion if True.

        Raises:
            HTTPException: If SQLAlchemyError occurs.
        """
        try:
            await session.delete(task)
            if commit_on:
                await session.commit()
        except SQLAlchemyError as error:
            await session.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f'Server error: {str(error)}'
            )
