from typing import Optional

from typing import List
from fastapi import (APIRouter, Path, Query, HTTPException, Body, Response,
                     status)
from sqlalchemy.exc import IntegrityError

from ..exceptions.utils import IntegrityErrorHandler
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

@router.get(
    "/id/{exercise_id}",
    summary='Get exercise by id',
    response_model=se.ExerciseAggregate
)
async def get_exercise(
    exercise_id: int = Path(
        description='exercise id'
    )
):
    exercise = await ExerciseRepository.get_by_id(exercise_id=exercise_id)
    if not exercise:
        raise HTTPException(status_code=404, detail="Exercise not found")

    return exercise


@router.post(
    "",
    summary='Create exercise',
    response_model=se.ExerciseAggregate
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
    response_model=se.ExerciseAggregate
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

@router.post(
    "/link",
    summary='Add link to exercise',
    status_code=201
)
async def add_link_to_exercise(
    exercise_id: int = Query(
        description='exercise id'
    ),
    link_id: int = Query(
        description='link id'
    )
):
    try:
        await ExerciseRepository.add_link(
            exercise_id=exercise_id,
            link_id=link_id
        )
    except IntegrityError as e:
        detail = IntegrityErrorHandler.handle_integrity_error(e)
        raise HTTPException(status_code=404, detail=detail)

    return Response(status_code=status.HTTP_201_CREATED)


@router.delete(
    "/link",
    summary='Delete link from exercise',
    status_code=status.HTTP_204_NO_CONTENT
)
async def delete_link_from_exercise(
    exercise_id: int = Query(
        description='exercise id'
    ),
    link_id: int = Query(
        description='link id'
    )
):
    try:
        await ExerciseRepository.delete_link(
            exercise_id=exercise_id,
            link_id=link_id
        )
    except IntegrityError as e:
        detail = IntegrityErrorHandler.handle_integrity_error(e)
        raise HTTPException(status_code=404, detail=detail)

    return Response(status_code=status.HTTP_204_NO_CONTENT)


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

