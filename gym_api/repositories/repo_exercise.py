from datetime import datetime
from typing import Optional, List

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from .base import BaseRepository
from ..database.postgres.base import SessionProvider
from ..config import db
from ..managers import manager_exercise, manager_card



_session_provider = SessionProvider(
    async_mode=True,
    engine_settings={'pool_pre_ping': True},
    db_settings=db
)

class ExerciseRepository(BaseRepository):
    @classmethod
    @_session_provider
    async def get_exercises_or_desc_by_master(
            cls,
            master_id: int,
            model,
            search: Optional[str] = None,
            session: AsyncSession = None
    ):
        manager =  manager_card.CardManager
        card_model = manager_card.CardManager.model

        query = select(model).where(
            card_model.master_id.in_([1, master_id])
        )

        if search:
            query = query.where(model.title.ilike(f'%%{search}%%'))

        query = query.order_by(model.title)

        return await manager.get_all(statement=query, session=session)

    @classmethod
    @_session_provider
    async def get_exercises_by_master(
            cls,
            master_id: int,
            search: Optional[str] = None,
            session: AsyncSession = None
    ):
        return await cls.get_exercises_or_desc_by_master(
            master_id=master_id,
            model=manager_exercise.ExerciseManager.model,
            search=search,
            session=session
        )

    @classmethod
    @_session_provider
    async def get_exercises_desc_by_master(
            cls,
            master_id: int,
            search: Optional[str] = None,
            session: AsyncSession = None
    ):
        return await cls.get_exercises_or_desc_by_master(
            master_id=master_id,
            model=manager_exercise.ExerciseDescManager.model,
            search=search,
            session=session
        )
