from typing import Optional

from typing import List
from fastapi import APIRouter, Path, Query, HTTPException, Body

from ..repositories.repo_exercise import ExerciseRepository
from ..schemas.schema_exercise import ExerciseDesc, Exercise


router = APIRouter(prefix='/exercise')


@router.get(
    "/{master_id}/exercises",
    summary='Getting a list of exercise by master_id',
    response_model=List[Exercise]
)
async def get_list_of_exercise(
    master_id: int,
    search: Optional[str] = Query(
        None,
        description="Поиск по названию упражнения"
    )
):
    return await ExerciseRepository.get_exercises_by_master(
        master_id=master_id,
        search=search
    )


@router.get(
    "/{exercise_id}/descriptions",
    summary='Getting a list of exercise description by exercise_id',
    response_model=List[ExerciseDesc],
)
async def get_list_of_exercise_description(
    master_id: int,
    search: Optional[str] = Query(
        None,
        description="Поиск по названию описания упражнения"
    )
):
    return await ExerciseRepository.get_exercises_desc_by_master(
        master_id=master_id,
        search=search
    )
