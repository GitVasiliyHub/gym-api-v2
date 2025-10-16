from typing import Optional

from typing import List
from fastapi import (
    APIRouter, Path, Query, HTTPException, Body, status, Response
)
from sqlalchemy.exc import IntegrityError

from ..exceptions.utils import IntegrityErrorHandler
from ..repositories.gym import GymRepository
from ..repositories.repo_task_group import TaskGroupRepository
from ..schemas import schema_task_group as stg


router = APIRouter(prefix='/task_group')


@router.post(
    "",
    summary='Creating task group',
    response_model=stg.TaskGroup
)
async def create_task_group(
    master_id: int = Query(
        ...,
        description='master id'
    ),
    gymer_id: int = Query(
        ...,
        description='gymer id'
    ),
    title: Optional[str] = Query(
        None,
        description='title'
    )
):
    try:
        return await TaskGroupRepository.create(
            master_id=master_id,
            gymer_id=gymer_id,
            title=title
        )
    except IntegrityError as e:
        detail = IntegrityErrorHandler.handle_integrity_error(e)
        raise HTTPException(status_code=404, detail=detail)


@router.get(
    "",
    summary='Getting a list of task group',
    response_model=List[stg.TaskGroupAggregate]
)
async def list_task_group(
    master_id: Optional[int] = Query(
        None,
        description='master id'
    ),
    gymer_id: int = Query(
        ...,
        description='gymmer id'
    ),
    status: stg.TaskGroupStatus = Query(
        stg.TaskGroupStatus.planned,
        description='Статус task_group'
    )
):
    try:
        task_groups = await TaskGroupRepository.get_task_groups(
            master_id=master_id,
            gymer_id=gymer_id,
            status=status
        )
    except IntegrityError as e:
        detail = IntegrityErrorHandler.handle_integrity_error(e)
        raise HTTPException(status_code=404, detail=detail)
    if not task_groups:
        raise HTTPException(status_code=404, detail="Task groups not found")
    return task_groups


@router.put(
    "/reorder",
    summary='Change order position task_group',
    status_code=status.HTTP_202_ACCEPTED
)
async def reorder_task_group(
    ordered_ids: List[stg.TaskGroupOrderIndex]
):
    await TaskGroupRepository.reorder_task_group(ordered_ids)

    return Response(status_code=200)


@router.put(
    "/{task_group_id}/status",
    summary='update task_group status',
    status_code=status.HTTP_202_ACCEPTED
)
async def update_task_group_status(
        task_group_id: int = Path(
            ...,
            description='task_group_id'
        ),
        status_name: stg.TaskGroupStatus = Query(
            ...,
            description='status task_group'
        )
):
    await TaskGroupRepository.update_status(
        task_group_id=task_group_id,
        status=status_name
    )

    return Response(status_code=202)


@router.put(
    "/{task_group_id}/title",
    summary='update task_group title',
    status_code=status.HTTP_202_ACCEPTED
)
async def update_task_group_title(
        task_group_id: int = Path(
            ...,
            description='task_group_id'
        ),
        title: Optional[str] = Query(
            ...,
            description='title task_group'
        )
):
    await TaskGroupRepository.update_title(
        task_group_id=task_group_id,
        title=title
    )

    return Response(status_code=202)



@router.post(
    "/copy/{task_group_id}",
    summary='Creating task group',
    response_model=stg.TaskGroupAggregate
)
async def copy_task_group(
    task_group_id: int = Path(
        ...,
        description='task group id'
    )
):
    new_task_group_id = await TaskGroupRepository.copy(
        task_group_id=task_group_id
    )
    if not new_task_group_id:
        raise HTTPException(status_code=404, detail="Task groups not found")

    return await TaskGroupRepository.get_by_id(
        task_group_id=new_task_group_id
    )
