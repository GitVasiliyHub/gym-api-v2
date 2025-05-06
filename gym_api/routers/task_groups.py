from typing import Optional

from typing import List
from fastapi import APIRouter, Path, Query, HTTPException, Body

from ..repositories.gym import GymRepository
from ..schemas.task import TaskGroup, TaskGroupCreate


router = APIRouter(prefix='/task_group')


@router.post(
    "",
    summary='Creating task group',
    response_model=TaskGroup
)
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


@router.get(
    "",
    summary='Getting a list of task group',
    response_model=List[TaskGroup]
)
async def list_task_group(
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