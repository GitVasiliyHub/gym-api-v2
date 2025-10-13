from datetime import datetime
from typing import Optional, List

from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession

from .base import BaseRepository
from ..database.postgres.base import SessionProvider
from ..config import db
from ..manager import manager_task_group as mtg
from ..repositories.repo_task import TaskRepository
from ..schemas import schema_task_group as stg



_session_provider = SessionProvider(
    async_mode=True,
    engine_settings={'pool_pre_ping': True},
    db_settings=db
)

class TaskGroupRepository(BaseRepository):
    @classmethod
    @_session_provider
    async def reorder_task_group(
            cls,
            ordered_ids: List[stg.TaskGroupOrderIndex],
            session: AsyncSession = None
    ):
        await session.execute(
            update(mtg.TaskGroupManager.model),
            [
                {
                    "task_group_id": data.task_group_id,
                    "order_idx": data.order_idx,
                    "update_dttm": datetime.now()
                }
                for data in ordered_ids
            ]

        )
        await session.commit()

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

    @classmethod
    @_session_provider
    async def get_by_id(
            cls,
            task_group_id: int,
            session: AsyncSession = None
    ):
        manager = mtg.TaskGroupManager
        where_exp = [
            manager.model.task_group_id == task_group_id
        ]

        return await manager.get_scalar_by_where(
            where_exp=where_exp,
            session=session
        )


    @classmethod
    @_session_provider
    async def copy(
            cls,
            task_group_id: int,
            session: AsyncSession = None
    ) -> Optional[int]:
        current_tg = await cls.get_by_id(
            task_group_id=task_group_id,
            session=session
        )

        if not current_tg: return None

        current_tg = stg.TaskGroupAggregate.model_validate(current_tg)
        try:
            new_tg = await mtg.TaskGroupManager.create(
                session=session,
                master_id=current_tg.master_id,
                gymer_id=current_tg.gymer_id,
                commit=False
            )
            new_tg_id = new_tg.task_group_id

            for current_task in current_tg.tasks:
                new_t = await TaskRepository.create_task(
                    task_group_id=new_tg_id,
                    exercise_id=current_task.exercise_id,
                    commit=False,
                    session=session
                )
                new_t_props = await TaskRepository.create_task_properties(
                    task_id=new_t.task_id,
                    min_weight=current_task.task_properties.min_weight,
                    max_weight=current_task.task_properties.max_weight,
                    rest=current_task.task_properties.rest,
                    commit=False,
                    session=session
                )
                # for set_item in current_task.task_properties.sets:
        except Exception as e:
            await session.rollback()
            raise e
        else:
            await session.commit()

        return new_tg_id
