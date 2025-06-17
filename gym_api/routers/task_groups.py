from typing import Optional

from typing import List
from fastapi import (
    APIRouter, Path, Query, HTTPException, Body, status, Response
)

from ..repositories.gym import GymRepository
from ..schemas.task import (
    TaskGroup, 
    TaskGroupCreate, 
    TaskGroupStatus, 
    TaskGroupWithTasks,
    TaskGroupOrderIndex
)


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
    response_model=List[TaskGroupWithTasks]
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
    status: TaskGroupStatus = Query(
        TaskGroupStatus.planned,
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


@router.post(
    "/copy/{task_group_id}",
    summary='Creating task group',
    response_model=TaskGroupWithTasks
)
async def copy_task_group(
    task_group_id: int = Path(
        ...,
        description='task group id'
    ),
    master_id: int = Query(
        ...,
    description='master id'
    )
):
  
    return await GymRepository.copy_task_group(
        task_group_id=task_group_id
    )
    
    
@router.put(
    "/reorder",
    summary='Change order position task_group',
    status_code=status.HTTP_202_ACCEPTED
)
async def reorder_task_group(
    ordered_ids: List[TaskGroupOrderIndex]
):
    await GymRepository.reorder_task_group(ordered_ids)
    
    return Response(status_code=200)
    