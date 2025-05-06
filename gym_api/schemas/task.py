from datetime import datetime
from typing import Optional, List, Dict

from pydantic import BaseModel, Field, ConfigDict


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
    status: str
    
    model_config = ConfigDict(from_attributes=True)

class TaskBase(BaseModel):
    task_group_id: int
    exercise_desc_id: int
    properties: dict
    status: str = 'planned'

class TaskCreate(TaskBase):
    pass

class Task(TaskBase):
    task_id: int
    create_dttm: datetime
    update_dttm: Optional[datetime]
    
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
    status: str
    create_dttm: datetime
    update_dttm: Optional[datetime]
    exercise_desc: ExerciseDescSimple

    model_config = ConfigDict(from_attributes=True)

class TaskGroupWithTasks(BaseModel):
    task_group_id: int
    status: str
    create_dttm: datetime
    update_dttm: Optional[datetime]
    num: Optional[int]
    start_dttm: Optional[datetime]
    task: List[TaskWithExercise]

    model_config = ConfigDict(from_attributes=True)
    
class TaskUpdate(BaseModel):
    exercise_desc_id: Optional[int]
    properties: Optional[Dict]
    