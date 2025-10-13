from typing import Optional, Any, List
from datetime import datetime
from enum import Enum

from pydantic import BaseModel, ConfigDict, Field
from .schema_exercise import ExerciseAggregate



class TaskOrderIndex(BaseModel):
    task_id: int
    order_idx: int


class TaskStatus(str, Enum):
    planned = 'planned'
    running = 'running'
    finished = 'finished'
    delete = 'delete'


class TaskBase(BaseModel):
    task_id: int
    task_group_id: int
    exercise_id: Optional[int]
    status: TaskStatus
    create_dttm: datetime
    update_dttm: Optional[datetime]
    order_idx: Optional[int]

    model_config = ConfigDict(from_attributes=True)


class Task(BaseModel):
    task_id: int
    task_group_id: int
    exercise_id: Optional[int]
    status: TaskStatus
    create_dttm: datetime
    update_dttm: Optional[datetime]
    order_idx: Optional[int]

    exercise: Optional[ExerciseAggregate] = Field(
        default=None
    )

    model_config = ConfigDict(from_attributes=True)


class TaskProperties(BaseModel):
    task_properties_id: int
    task_id: int
    max_weight: Optional[float]
    min_weight: Optional[float]
    rest: Optional[int]

    model_config = ConfigDict(from_attributes=True)


class Set(BaseModel):
    set_id: int
    task_properties_id: int
    fact_value: Optional[float]
    fact_rep: Optional[int]
    plan_value: Optional[float]
    plan_rep: Optional[int]

    model_config = ConfigDict(from_attributes=True)


class TaskPropertiesAggregate(TaskProperties):
    sets: List[Set] = Field(
        default_factory=list
    )
    model_config = ConfigDict(from_attributes=True)


class TaskAggregate(Task):
    task_properties: Optional[TaskPropertiesAggregate] = Field(
        default=None
    )
    model_config = ConfigDict(from_attributes=True)


class TaskPropertiesUpdate(BaseModel):
    max_weight: Optional[float]
    min_weight: Optional[float]
    rest: Optional[int]


class SetUpdate(BaseModel):
    set_id: Optional[int] = None
    fact_value: Optional[float] = None
    fact_rep: Optional[int] = None
    plan_value: Optional[int] = None
    plan_rep: Optional[int] = None


class TaskPropertiesAggregateUpdate(TaskPropertiesUpdate):
    sets: List[SetUpdate] = Field(
        default_factory=list
    )


class UpdateTask(BaseModel):
    task_id: int
    exercise_id: int
    status: Optional[TaskStatus]
    task_properties: Optional[TaskPropertiesAggregateUpdate] = Field(
        default=None
    )

