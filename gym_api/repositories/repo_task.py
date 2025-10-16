from datetime import datetime
from typing import Optional, List

from sqlalchemy import select, update, and_
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
    async def update(
            cls,
            task: st.UpdateTask,
            session: AsyncSession = None
    ):
        commit = False
        manager = mt.TaskManager
        current_task = await manager.get_scalar_by_where(
            where_exp=[manager.model.task_id == task.task_id],
            session=session
        )
        if not current_task:
            raise HTTPException(404, f'Task {task.task_id} not found')

        current_task = st.TaskAggregate.model_validate(current_task)
        current_sets = [
            s.set_id for s in current_task.task_properties.sets
        ]
        new_sets = [
            s.set_id for s in task.task_properties.sets if s.set_id
        ]
        delete_sets = set(current_sets) - set(new_sets)

        if delete_sets:
            for set_id in delete_sets:
                await mt.SetManager.delete(
                    where_cond=and_(mt.SetManager.model.set_id == set_id),
                    session=session,
                    commit=False
                )
                commit = True
        update_task_values = {}

        if current_task.update_dttm is None:
            update_task_values['status'] = st.TaskStatus.running

        if task.exercise_id != current_task.exercise_id:
            update_task_values['exercise_id'] = task.exercise_id

        if task.status != current_task.status:
            update_task_values['status'] = task.status

        if update_task_values:
            update_task_values['update_dttm'] = datetime.now()
            model = mt.TaskManager.model
            stmt = (
                update(model)
                .where(model.task_id == current_task.task_id)
                .values(update_task_values)
            )
            await session.execute(stmt)
            commit = True

        if task.task_properties:
            await mt.TaskPropertiesManager.update(
                conditions=[
                    mt.TaskPropertiesManager.model.task_properties_id ==
                    current_task.task_properties.task_properties_id
                ],
                session=session,
                commit=False,
                min_weight=task.task_properties.min_weight,
                max_weight=task.task_properties.max_weight,
                rest=task.task_properties.rest
            )
            commit = True

            for s in task.task_properties.sets:
                if s.set_id in new_sets:
                    await mt.SetManager.update(
                        conditions=[
                            mt.SetManager.model.set_id == s.set_id
                        ],
                        session=session,
                        commit=False,
                        fact_value=s.fact_value,
                        fact_rep=s.fact_rep,
                        plan_value=s.plan_value,
                        plan_rep=s.plan_rep

                    )
                    commit = True
                    continue

                await mt.SetManager.create(
                    commit=False,
                    session=session,
                    task_properties_id=current_task.task_properties
                    .task_properties_id,
                    fact_value=s.fact_value,
                    fact_rep=s.fact_rep,
                    plan_value=s.plan_value,
                    plan_rep=s.plan_rep
                )
                commit = True

        if commit:
            await session.commit()

        return await manager.get_scalar_by_where(
            where_exp=[manager.model.task_id == task.task_id],
            session=session
        )


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
            commit: bool = False,
            session: AsyncSession = None,
            **kwargs
    ):
        try:
            task_manager = mt.TaskManager
            task = await task_manager.create(
                task_group_id=task_group_id,
                commit=commit,
                session=session,
                **kwargs
            )

            task = st.TaskBase.model_validate(task)
            task_a = st.TaskAggregate.model_validate(task)
        except Exception as e:
            await session.rollback()
            raise e
        else:
            if commit:
                await session.commit()

        return task_a

    @classmethod
    @_session_provider
    async def create_task_properties(
            cls,
            task_id: int,
            commit: bool = False,
            session: AsyncSession = None,
            **kwargs
    ):
        try:
            task_props_manager = mt.TaskPropertiesManager
            task_props = await task_props_manager.create(
                session=session,
                commit=commit,
                task_id=task_id,
                **kwargs
            )
            task_props = st.TaskProperties.model_validate(task_props)
        except Exception as e:
            await session.rollback()
            raise e
        else:
            if commit:
                await session.commit()

        return task_props

    @classmethod
    @_session_provider
    async def create(
            cls,
            task_group_id: int,
            session: AsyncSession = None
    ):
        try:
            task_a = await cls.create_task(
                task_group_id=task_group_id,
                commit=False,
                session=session
            )
            task_props = await cls.create_task_properties(
                task_id=task_a.task_id,
                commit=False,
                session=session
            )
            task_a.task_properties = st.TaskPropertiesAggregate.model_validate(
                task_props
            )
        except Exception as e:
            await session.rollback()
            raise e
        else:
            await session.commit()

        return task_a
