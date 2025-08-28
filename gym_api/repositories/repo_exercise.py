from datetime import datetime, UTC
from typing import Optional, List

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from .base import BaseRepository
from ..database.postgres.base import SessionProvider
from ..config import db
from ..managers import manager_exercise as me
from ..managers import manager_link as ml
from ..schemas import schema_exercise as se
from ..schemas import schema_link as sl



_session_provider = SessionProvider(
    async_mode=True,
    engine_settings={'pool_pre_ping': True},
    db_settings=db
)

class ExerciseRepository(BaseRepository):
    @classmethod
    @_session_provider
    async def get_exercises_by_master(
            cls,
            master_id: int,
            search: Optional[str] = None,
            session: AsyncSession = None
    ):
        manager = me.ExerciseManager
        model = me.ExerciseManager.model

        query = select(model).where(model.master_id.in_([1, master_id]))

        if search:
            query = query.where(model.exercise_name.ilike(f'%%{search}%%'))

        query = query.order_by(model.exercise_name)

        return await manager.get_all(statement=query, session=session)

    @classmethod
    @_session_provider
    async def create(
            cls,
            exercise: se.CreateExercise,
            session: AsyncSession = None
    ) -> se.ExerciseAggregate:
        new_exercise = await me.ExerciseManager.create(
            session=session,
            master_id=exercise.master_id,
            exercise_name=exercise.exercise_name,
            description=exercise.description,
            create_dttm=datetime.now(),
            status=se.ExerciseStatus.active
        )
        new_exercise = se.ExerciseAggregate.model_validate(new_exercise)

        if exercise.link_ids:
            for link_id in exercise.link_ids:
                await ml.LinkExerciseManager.create(
                    session=session,
                    exercise_id=new_exercise.exercise_id,
                    link_id=link_id
                )
            links = await ml.LinkManager.get_all_by_where(
                session=session,
                where_exp=[ml.LinkManager.model.link_id.in_(
                    exercise.link_ids)]
            )
            new_exercise.links = [
                sl.Link.model_validate(link) for link in links
            ]
        return new_exercise


    @classmethod
    @_session_provider
    async def update(
            cls,
            exercise: se.Exercise,
            session: AsyncSession = None
    ) -> Optional[se.ExerciseAggregate]:

        current_ex = await session.get(
            me.ExerciseManager.model, exercise.exercise_id
        )
        if not current_ex:
            return None

        current_ex.status = exercise.status
        current_ex.exercise_name = exercise.exercise_name
        current_ex.description = exercise.description
        current_ex.update_dttm = datetime.now(UTC)

        await session.commit()
        await session.refresh(current_ex)
        new_exercise = se.ExerciseAggregate.model_validate(current_ex)

        return new_exercise

    @classmethod
    @_session_provider
    async def copy(
            cls,
            exercise_id: int,
            session: AsyncSession = None
    ) -> Optional[se.ExerciseAggregate]:
        original_ex = await session.get(me.ExerciseManager.model, exercise_id)

        if not original_ex:
            return None
        original_ex = se.Exercise.model_validate(original_ex)
        where_exp = [ml.LinkExerciseManager.model.exercise_id == exercise_id]

        original_link_ex = await ml.LinkExerciseManager.get_all_by_where(
            session=session,
            where_exp=where_exp
        )

        link_ids = [obj.link_id for obj in original_link_ex]

        return await cls.create(
            session=session,
            exercise=se.CreateExercise(
                master_id=original_ex.master_id,
                exercise_name=original_ex.exercise_name,
                description=original_ex.description,
                link_ids=link_ids
            )
        )
