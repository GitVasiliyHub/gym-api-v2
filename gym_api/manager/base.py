from typing import TypeVar, Generic, List

from sqlalchemy import update, select, delete
from sqlalchemy.ext.asyncio import AsyncSession

T = TypeVar('T')


class Manager:
    model: Generic[T]

    @classmethod
    async def create(
            cls, session: AsyncSession, commit=True, **kwargs
    ) -> Generic[T]:
        model = cls.model(**kwargs)
        session.add(model)
        if commit:
            await session.commit()
            await session.refresh(model)
        else:
            await session.flush()

        return model

    @classmethod
    async def update(
            cls, conditions: list, session: AsyncSession, **kwargs
    ) -> Generic[T]:
        statement = (
            update(cls.model).where(*conditions).values(**kwargs)
        )

        await session.execute(statement)
        await session.commit()

    @classmethod
    async def get_all(
            cls,
            session: AsyncSession,
            limit: int = 0,
            offset: int = 0,
            statement=None
    ):
        if statement is None:
            statement = select(cls.model)

        if limit:
            statement = statement.limit(limit)

        if offset:
            statement = statement.offset(offset)

        result = await session.execute(statement)

        return result.scalars().all()

    @classmethod
    async def get_scalar(cls, statement, session: AsyncSession):
        result = await session.execute(statement)
        return result.scalar()

    @classmethod
    async def delete(cls, uuid: str, session: AsyncSession):
        statement = delete(cls.model).where(cls.model.id == uuid)

        await session.execute(statement)
        await session.commit()

    @classmethod
    async def get_scalar_by_where(
            cls, where_exp: List, session: AsyncSession
    ):
        statement = select(cls.model).where(*where_exp)
        return await cls.get_scalar(statement=statement, session=session)

    @classmethod
    async def get_all_by_where(
            cls,
            where_exp: List,
            session: AsyncSession,
            limit: int = None,
            offset: int = None
    ):
        statement = select(cls.model).where(*where_exp)
        return await cls.get_all(
            statement=statement,
            limit=limit,
            offset=offset,
            session=session
        )
