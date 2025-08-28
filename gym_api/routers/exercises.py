from typing import Optional

from typing import List
from fastapi import APIRouter, Path, Query, HTTPException, Body

from ..repositories.repo_exercise import ExerciseRepository
from ..schemas import schema_exercise as se


router = APIRouter(prefix='/exercise')


@router.get(
    "/{master_id}",
    summary='Getting a list of exercise by master_id',
    response_model=List[se.Exercise]
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


@router.post(
    "",
    summary='Create exercise',
    response_model=List[se.ExerciseAggregate]
)
async def create_exercise(
    exercise: se.CreateExercise = Body(
        description='Exercise data'
    )
):
    return await ExerciseRepository.create(exercise=exercise)


@router.post(
    "/copy/{exercise_id}",
    summary='Copy exercise',
    response_model=List[se.ExerciseAggregate]
)
async def copy_exercise(
    exercise_id: int = Path(
        description='exercise id'
    )
):
    new_exercise = await ExerciseRepository.copy(exercise_id=exercise_id)
    if not new_exercise:
        raise HTTPException(status_code=404, detail="Exercise not found")

    return new_exercise


@router.put(
    "",
    summary='Update exercise',
    response_model=List[se.ExerciseAggregate]
)
async def update_exercise(
    exercise: se.Exercise = Body(
        description='Exercise data'
    )
):
    new_ex = await ExerciseRepository.update(exercise=exercise)
    if not new_ex:
        raise HTTPException(status_code=404, detail="Exercise not found")

    return new_ex

