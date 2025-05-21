import json
from typing import Optional

from typing import List
from fastapi import APIRouter, Path, Query, HTTPException, Body

from ..repositories.gym import GymRepository
from ..schemas.task import (
    Task, 
    TaskCreate,  
    TaskUpdate,
    TaskGroupWithTasks
)


router = APIRouter(prefix='/task')



@router.post(
    "",
    summary='Creating a new task',
    response_model=Task
)
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


@router.put(
    "/{task_id}",
    summary='Updating task by task_id',
    response_model=Task
)
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
        exercise_desc_id=task_update.exercise_desc_id,
        status=task_update.status,
        properties=task_update.properties
    )
    if not updated_task:
        raise HTTPException(status_code=404, detail="Task not found")
    return updated_task


@router.get(
    "/{gymer_id}/history",
    summary='Getting training history by master_id and gymmer_id',
    response_model=List[TaskGroupWithTasks]
)
async def get_master_task_groups_with_tasks(
    gymer_id: int = Path(
        ...
    ),
    master_id: Optional[int] = Query(
        None
    ),
    page_no: int = Query(1, description='Номер страницы'),
    page_size: int = Query(100, description='Размер страницы'),
    # current_master: dict = Depends(get_current_master),
):
    # Фильтрация по мастеру и дополнительным параметрам
    limit = page_size
    offset = (page_no - 1) * page_size
    
    return await GymRepository.get_master_task_groups_with_tasks(
        master_id=master_id,
        gymer_id=gymer_id,
        limit=limit,
        offset=offset
    )
