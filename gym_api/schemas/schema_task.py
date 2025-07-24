from typing import Optional, Any
from datetime import datetime
from enum import Enum

from pydantic import BaseModel, ConfigDict

class TaskStatus(str, Enum):
    planned = 'planned'
    running = 'running'
    finished = 'finished'


class Task(BaseModel):
    task_id: int
    task_group_id: int
    status: TaskStatus
    create_dttm: datetime
    update_dttm: Optional[datetime]
    order_idx: Optional[int]

    model_config = ConfigDict(from_attributes=True)


class TaskProperties(BaseModel):
    task_id: int
    max_weight: Optional[float]
    min_weight: Optional[float]
    rest: Optional[int]

    model_config = ConfigDict(from_attributes=True)


class Set(BaseModel):
    set_id: int
    task_properties_id: int
    fact_value: Any
    fact_rep: Any
    plan_value: Any
    plan_rep: Any
