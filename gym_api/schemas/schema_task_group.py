from typing import Optional
from datetime import datetime
from enum import Enum

from pydantic import BaseModel, ConfigDict

from .schema_user import Master, Gymer


class TaskGroupOrderIndex(BaseModel):
    task_group_id: int
    order_idx: int


class TaskOrderIndex(BaseModel):
    task_id: int
    order_idx: int


class TaskGroupStatus(str, Enum):
    planned = 'planned'
    running = 'running'
    finished = 'finished'


class TaskGroup(BaseModel):
    task_group_id: int
    master_id: int
    gymer_id: int
    status: TaskGroupStatus
    create_dttm: datetime
    update_dttm: Optional[datetime]
    start_dttm: Optional[datetime]
    order_idx: Optional[int]

    model_config = ConfigDict(from_attributes=True)


class TaskGroupAggregate(BaseModel):
    master: Master
    gymer: Gymer

    model_config = ConfigDict(from_attributes=True)
