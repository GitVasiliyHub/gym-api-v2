from datetime import datetime
from typing import Optional, List

from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException

from .base import BaseRepository
from ..database.postgres.base import SessionProvider
from ..config import db
from ..manager import manager_task as mt
from ..schemas import schema_task as st


_session_provider = SessionProvider(
    async_mode=True,
    engine_settings={'pool_pre_ping': True},
    db_settings=db
)

class TaskRepository(BaseRepository):
    @classmethod
    @_session_provider
    async def reorder_task(
            cls,
            ordered_ids: List[st.TaskOrderIndex],
            session: AsyncSession = None
    ):
        await session.execute(
            update(mt.TaskManager.model),
            [
                {
                    "task_id": data.task_id,
                    "order_idx": data.order_idx,
                    "update_dttm": datetime.now()
                }
                for data in ordered_ids
            ]

        )
        await session.commit()


    @classmethod
    @_session_provider
    async def get_tasks_by_group(
            cls,
            task_group_id: int,
            session: AsyncSession = None
    ):
        manager = mt.TaskManager
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
        try:
            task_manager = mt.TaskManager
            task_props_manager = mt.TaskPropertiesManager
            task = await task_manager.create(
                task_group_id=task_group_id,
                commit=False,
                session=session
            )
            task = st.Task.model_validate(task)
            task_a = st.TaskAggregate.model_validate(task)
            task_props = await task_props_manager.create(
                session=session,
                commit=False,
                task_id=task_a.task_id
            )
            task_props = st.TaskProperties.model_validate(task_props)
            task_a.task_properties = st.TaskPropertiesAggregate.model_validate(
                task_props
            )
        except Exception as e:
            print(e)
            await session.rollback()
            raise HTTPException(status_code=500, detail="Internal server error")
        else:
            await session.commit()

        return task_a
