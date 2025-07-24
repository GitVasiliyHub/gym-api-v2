from datetime import datetime
from typing import Optional, List

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from .base import BaseRepository
from ..database.postgres.base import SessionProvider
from ..config import db
from ..managers import manager_card as card_manager
from ..schemas import user as user_schema



_session_provider = SessionProvider(
    async_mode=True,
    engine_settings={'pool_pre_ping': True},
    db_settings=db
)

class CardRepository(BaseRepository):
    @classmethod
    @_session_provider
    async def get_tasks_by_group(
            cls,
            task_group_id: int,
            session: AsyncSession = None
    ):
        t = model.Task
        stmt = select(t).where(t.task_group_id == task_group_id)

        result = await session.execute(stmt)

        return result.scalars().all()
