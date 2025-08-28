from datetime import datetime
from typing import Optional, List

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from .base import BaseRepository
from ..database.postgres.base import SessionProvider
from ..config import db
from ..managers import manager_task



_session_provider = SessionProvider(
    async_mode=True,
    engine_settings={'pool_pre_ping': True},
    db_settings=db
)

class TaskRepository(BaseRepository):
    @classmethod
    @_session_provider
    async def get_tasks_by_group(
            cls,
            task_group_id: int,
            session: AsyncSession = None
    ):
        manager = manager_task.TaskManager
        return await manager.get_all_by_where(
            where_exp=[manager.model.task_group_id == task_group_id],
            session=session
        )

    @classmethod
    @_session_provider
    async def create_task(
            cls,
            task_group_id: int,
            session: AsyncSession = None
    ):
        manager = manager_task.TaskManager
        return await manager.create(
            task_group_id=task_group_id,
            session=session
        )