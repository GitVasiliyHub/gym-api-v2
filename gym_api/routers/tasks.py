import json
from typing import Optional

from typing import List
from fastapi import APIRouter, Path, Query, HTTPException, Body

from ..repositories.gym import GymRepository
from ..schemas.task import (
    Task, 
    TaskGroup, 
    TaskCreate, 
    TaskGroupCreate, 
    TaskUpdate,
    Exercise,
    ExerciseDescSimple
)


router = APIRouter(prefix='/task')


@router.post("/task_group", response_model=TaskGroup)
async def create_task_group(
    master_id: int = Query(
        ...,
        description='master id'
    ),
    task_group: TaskGroupCreate = Body(
        ...,
        description='Параметры создания task_group'
    ),
    # current_master: dict = Depends(get_current_master)
):
    return await GymRepository.create_task_group(
        master_id=master_id,
        gymer_id=task_group.gymer_id,
        properties=task_group.properties
    )
    
@router.post("", response_model=Task)
async def create_task(
    task: TaskCreate = Body(
        ...,
        description='Параметры создания task'
    )
    # current_master: dict = Depends(get_current_master)
):

    task_group = await GymRepository.get_task_group_by_id(task.task_group_id)
    if not task_group:
    # if not task_group or task_group.master_id != current_master["master_id"]:
        raise HTTPException(
                status_code=404,
                detail="Task group not found or access denied"
            )

    return await GymRepository.create_task(
        task_group_id=task.task_group_id,
        exercise_desc_id=task.exercise_desc_id,
        properties=task.properties
    )


@router.put("/{task_id}", response_model=Task)
async def update_task(
    task_id: int = Path(
        ...,
        description='task_id'
    ),
    task_update: TaskUpdate = Body(
        ...,
        description='Параметры обновлния'
    ),
    # current_master: dict = Depends(get_current_master)
):
    # Проверяем принадлежность задачи мастеру

    updated_task = await GymRepository.update_task(
        task_id=task_id,
        status=task_update.status,
        properties=task_update.properties
    )
    if not updated_task:
        raise HTTPException(status_code=404, detail="Task not found")
    return updated_task

@router.get("/task_groups", response_model=List[TaskGroup])
async def get_tasks_by_group(
    master_id: Optional[int] = Query(
        None,
        description='master id'
    ),
    gymer_id: Optional[int] = Query(
        None,
        description='gymmer id'
    ),
    status: str = Query(
        'planned',
        description='Статус task_group'
    )
    # current_master: dict = Depends(get_current_master)
):
    if master_id is None and gymer_id is None:
        raise HTTPException(
            status_code=400,
            detail="Set master_id or gymmer_id or both"
            )
    task_groups = await GymRepository.get_task_groups(
        master_id=master_id,
        gymer_id=gymer_id,
        status=status    
    )
    if not task_groups:
        raise HTTPException(status_code=404, detail="Tasks not found")
    return task_groups
    
    
@router.get("/{task_group_id}/tasks", response_model=List[Task])
async def get_tasks_by_group(
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
    "/master/{master_id}/exercises",
    response_model=List[Exercise]
)
async def get_master_exercises(
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
    "/exercises/{exercise_id}/descriptions",
    response_model=List[ExerciseDescSimple],
)
async def get_exercise_description_ids(
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


@router.get("/master_history")
async def get_master_task_groups_with_tasks(
    # current_master: dict = Depends(get_current_master),
    page_no: int = Query(1, description='Номер страницы'),
    page_size: int = Query(100, description='Размер страницы'),
    gymer_id: Optional[int] = Query(None),
    master_id: Optional[int] = Query(None)
):
    # Фильтрация по мастеру и дополнительным параметрам
    limit = page_size
    offset = (page_no - 1) * page_size
    
    task_groups = await GymRepository.get_master_task_groups_with_tasks(
        master_id=master_id,
        gymer_id=gymer_id,
        limit=limit,
        offset=offset
    )
    
    return 
