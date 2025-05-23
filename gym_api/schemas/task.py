from datetime import datetime
from enum import Enum
from typing import Optional, List, Dict

from pydantic import BaseModel, Field, ConfigDict

class TaskGroupStatus(str, Enum):
    planned = 'planned'
    running = 'running'
    finished = 'finished'

class TaskProperties(BaseModel):
    max_weight: Optional[int] = Field(default=None)
    min_weight: Optional[int] = Field(default=None)
    rest: Optional[int] = Field(default=None)
    repeats: Optional[int] = Field(default=None)
    sets: Optional[int] = Field(default=None)
    

class TaskGroupBase(BaseModel):
    master_id: int
    gymer_id: int
    properties: dict = Field(default_factory=dict)

class TaskGroupCreate(BaseModel):
    gymer_id: int
    properties: dict = Field(default_factory=dict)

class TaskGroup(TaskGroupBase):
    task_group_id: int
    create_dttm: datetime
    update_dttm: Optional[datetime]
    start_dttm: Optional[datetime]
    num: Optional[int]
    status: TaskGroupStatus
    
    model_config = ConfigDict(from_attributes=True)

class TaskBase(BaseModel):
    task_group_id: int
    exercise_desc_id: int

class TaskCreate(TaskBase):
    pass

class Task(TaskBase):
    task_id: int
    create_dttm: datetime
    update_dttm: Optional[datetime]
    properties: TaskProperties
    
    model_config = ConfigDict(from_attributes=True)


class Exercise(BaseModel):
    exercise_id: int
    title: str
    master_id: int

    model_config = ConfigDict(from_attributes=True)
    
class ExerciseDescSimple(BaseModel):
    exercise_id: int
    exercise_desc_id: int
    description: str
    
    exercise: Exercise

    model_config = ConfigDict(from_attributes=True)

class TaskWithExercise(BaseModel):
    task_id: int
    create_dttm: datetime
    update_dttm: Optional[datetime]
    exercise_desc: ExerciseDescSimple
    properties: TaskProperties

    model_config = ConfigDict(from_attributes=True)

class TaskGroupWithTasks(BaseModel):
    task_group_id: int
    status: TaskGroupStatus
    create_dttm: datetime
    update_dttm: Optional[datetime]
    num: Optional[int]
    start_dttm: Optional[datetime]
    task: List[TaskWithExercise]

    model_config = ConfigDict(from_attributes=True)
    
class TaskUpdate(BaseModel):
    exercise_desc_id: Optional[int] = Field(None)
    properties: Optional[TaskProperties] = Field(default_factory=TaskProperties)
    