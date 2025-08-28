from uuid import UUID

from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError, SQLAlchemyError


class BaseCRUD:
    def __init__(self, model):
        self.model = model

    async def get_all(self, session: AsyncSession):
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
        return (
            await session.execute(
                select(self.model)
            ).where(self.model.uuid == uuid)
        ).scalar()

    async def create(
        self, 
        create_schema, 
        session: AsyncSession,
        commit_on: bool = True,
    ):
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
        try:
            await session.delete(task)
            if commit_on:
                await session.commit()
            return task
        except SQLAlchemyError as error:
            await session.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f'Server error: {str(error)}'
            )
