from typing import Optional, Any, List
from datetime import datetime
from enum import Enum

from pydantic import BaseModel, ConfigDict, Field



class TaskOrderIndex(BaseModel):
    task_id: int
    order_idx: int


class TaskStatus(str, Enum):
    planned = 'planned'
    running = 'running'
    finished = 'finished'


class Task(BaseModel):
    task_id: int
    task_group_id: int
    exercise_id: Optional[int]
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


class UpdateTask(BaseModel):
    task_id: int
    card_id: int
    status: Optional[TaskStatus]
    order_idx: Optional[int]

class TaskPropertiesAggregate(TaskProperties):
    sets: List[Set] = Field(
        default_factory=list
    )

class TaskAggregate(Task):
    task_properties: Optional[TaskPropertiesAggregate] = Field(
        default=None
    )
