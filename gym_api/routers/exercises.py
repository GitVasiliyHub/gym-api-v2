from typing import Optional

from typing import List
from fastapi import APIRouter, Path, Query, HTTPException, Body

from ..repositories.gym import GymRepository
from ..schemas.task import (
    Task, 
    Exercise,
    ExerciseDescSimple
)


router = APIRouter(prefix='/exercise')


@router.get(
    "/{task_group_id}/tasks",
    summary='Getgin a list of task by task_group_id',
    response_model=List[Task]
)
async def get_tasks_with_exercise_by_group(
    task_group_id: int = Path(
        ...,
        description='task_group id'
    ),
    # current_master: dict = Depends(get_current_master)
):
    # Здесь должна быть проверка, что task_group принадлежит текущему мастеру
    tasks = await GymRepository.get_tasks_by_group(task_group_id)
    if not tasks:
        raise HTTPException(status_code=404, detail="Tasks not found")
    return tasks


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
    ),
    # current_master: dict = Depends(get_current_master)
):
    # if master_id != current_master["master_id"]:
    #     raise HTTPException(status_code=403, detail="Forbidden")
    
    return await GymRepository.get_exercises_by_master(
        master_id=master_id,
        search=search
    )


@router.get(
    "/{exercise_id}/descriptions",
    summary='Getting a list of exercise description by exercise_id',
    response_model=List[ExerciseDescSimple],
)
async def get_list_of_exercise_description(
    exercise_id: int,
    # current_master: dict = Depends(get_current_master)
):
    # Проверяем принадлежность упражнения мастеру
    exercise = await GymRepository.get_exercise_by_id(exercise_id)
    if not exercise:
        raise HTTPException(
            status_code=404,
            detail="Exercise not found or access denied"
        )

    return await GymRepository.get_exercise_descriptions(exercise_id)
