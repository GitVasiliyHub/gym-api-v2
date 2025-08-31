from datetime import datetime
from typing import Optional, List

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from .base import BaseRepository
from ..database.postgres.base import SessionProvider
from ..config import db
from ..manager import manager_task_group as mtg
from ..schemas import schema_task_group as stg



_session_provider = SessionProvider(
    async_mode=True,
    engine_settings={'pool_pre_ping': True},
    db_settings=db
)

class TaskGroupRepository(BaseRepository):
    @classmethod
    @_session_provider
    async def create(
            cls,
            master_id: int,
            gymer_id: int,
            session: AsyncSession = None
    ):
        return await mtg.TaskGroupManager.create(
            session=session,
            master_id=master_id,
            gymer_id=gymer_id
        )


    @classmethod
    @_session_provider
    async def get_task_groups(
            cls,
            master_id: int,
            gymer_id: int,
            status: stg.TaskGroupStatus,
            session: AsyncSession = None
    ):
        manager = mtg.TaskGroupManager
        where_exp = [
            manager.model.gymer_id == gymer_id,
            manager.model.status == status
        ]
        if master_id:
            where_exp.append(manager.model.master_id == master_id)
        return await manager.get_all_by_where(
            where_exp=where_exp,
            session=session
        )