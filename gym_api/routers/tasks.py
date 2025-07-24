import json
from typing import Optional

from typing import List
from fastapi import (
    APIRouter, Path, Query, HTTPException, Body, status, Response
)

from ..repositories.gym import GymRepository
from ..repositories.repo_task import TaskRepository
from ..schemas.task import (
    Task,
    TaskGroup,
    TaskCreate,
    TaskUpdate,
    TaskProperties,
    TaskGroupStatus,
    TaskGroupWithTasks,
    TaskWithExercise,
    TaskOrderIndex
)


router = APIRouter(prefix='/task')


@router.get(
    "/{task_group_id}/tasks",
    summary='Getting a list of task by task_group_id',
    response_model=List[Task]
)
async def get_tasks_with_exercise_by_group(
    task_group_id: int = Path(
        ...,
        description='task_group id'
    )
):
    tasks = await TaskRepository.get_tasks_by_group(task_group_id)
    if not tasks:
        raise HTTPException(status_code=404, detail="Tasks not found")
    return tasks



@router.post(
    "",
    summary='Creating a new task',
    response_model=Task
)
async def create_task(
    task: TaskCreate = Body(
        ...,
        description='Параметры создания task'
    ),
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
        properties=task.properties.model_dump()
    )


@router.put(
    "/{task_id}/master_id",
    summary='Master updating task by task_id',
    response_model=Task
)
async def master_update_task(
    task_id: int = Path(
        ...,
        description='task_id'
    ),
    master_id: int = Query(
        ...,
        description='master_id'
    ),
    task_update: TaskUpdate = Body(
        ...,
        description='Параметры обновлния'
    ),
    # current_master: dict = Depends(get_current_master)
):
    # Проверяем принадлежность задачи мастеру
    
    task = await GymRepository.get_task_group_by_task_id(task_id)
    
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
 
    task_group_status = task.task_group.status
    
    if task_group_status != 'planned':
         raise HTTPException(
             status_code=403,
             detail=f"Task can't update, task_group_stasus {task_group_status}"
        )
        
    updated_task = await GymRepository.update_task(
        task_id=task_id,
        exercise_desc_id=task_update.exercise_desc_id,
        properties=task_update.properties.model_dump()
    )
    if not updated_task:
        raise HTTPException(status_code=404, detail="Task not found")
    return updated_task


@router.put(
    "/{task_id}/gymer_id",
    summary='Gymer updating task by task_id',
    response_model=Task
)
async def gymer_update_task(
    task_id: int = Path(
        ...,
        description='task_id'
    ),
    gymer_id: int = Query(
        ...,
        description='gymer_id'
    ),
    task_update: TaskUpdate = Body(
        ...,
        description='Параметры обновлния'
    ),
    # current_master: dict = Depends(get_current_master)
):
    # Проверяем принадлежность задачи gymer
   
    task = await GymRepository.get_task_group_by_task_id(task_id)
    
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
 
    task_group = TaskGroup.model_validate(task.task_group)
    
    if task_group.status not in (TaskGroupStatus.planned, TaskGroupStatus.running):
         raise HTTPException(
             status_code=403,
             detail="Task can't update, task_group_stasus {task_group.status}"
        )
  
    updated_task = await GymRepository.update_task(
        task_id=task_id,
        exercise_desc_id=task_update.exercise_desc_id,
        properties=task_update.properties.model_dump()
    )
        
    if not updated_task:
        raise HTTPException(status_code=404, detail="Task not found")
    
    if task_group.status == TaskGroupStatus.planned:
        await GymRepository.update_task_group_status(
            task_group_id=task_group.task_group_id,
            status=TaskGroupStatus.running
        )
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

@router.get(
    "/{task_id}",
    summary='Getting task by task_id',
    response_model=TaskWithExercise
    )
async def get_task_by_task_id(
        task_id: int = Path(
        ...,
        description='task_id'
    )
):
    task = await GymRepository.get_task_by_id(task_id=task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    
    return task


@router.put(
    "/reorder",
    summary='Change order position task',
    status_code=status.HTTP_202_ACCEPTED
)
async def reorder_task(
    ordered_ids: List[TaskOrderIndex]
):
    await GymRepository.reorder_task(ordered_ids)
    
    return Response(status_code=200)