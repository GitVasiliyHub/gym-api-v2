from datetime import datetime
from typing import Optional, List

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from .base import BaseRepository
from ..database.postgres.base import SessionProvider
from ..config import db
from ..managers import manager_task_group



_session_provider = SessionProvider(
    async_mode=True,
    engine_settings={'pool_pre_ping': True},
    db_settings=db
)

class TaskGroupRepository(BaseRepository):
    @classmethod
    @_session_provider
    async def get_task_group(
            cls,
            task_group_id: int,
            session: AsyncSession = None
    ):
        manager = manager_task_group.TaskGroupManager
        return await manager.get_scalar_by_where(
            where_exp=[manager.model.task_group_id == task_group_id],
            session=session
        )