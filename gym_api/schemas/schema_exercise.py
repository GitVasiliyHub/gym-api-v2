from enum import Enum
from typing import Optional, List
from datetime import datetime

from pydantic import BaseModel, ConfigDict


class ExerciseStatus(str, Enum):
    active = 'active'
    archive = 'archive'


class Exercise(BaseModel):
    exercise_id: int
    master_id: int
    exercise_name: Optional[str]
    description: Optional[str]
    status: ExerciseStatus = ExerciseStatus.active

    model_config = ConfigDict(from_attributes=True)


class LinkExercise(BaseModel):
    link_id: int
    exercise_id: int


class Link(BaseModel):
    link_id: int
    link: str
    title: Optional[str]


class ExerciseAggregate(Exercise):
    links: Optional[List[Link]]

    model_config = ConfigDict(from_attributes=True)


class CreateLink(BaseModel):
    link: str
    title: Optional[str]


class CreateExercise(BaseModel):
    master_id: int
    exercise_name: Optional[str]
    description: Optional[str]
    
    link_ids: Optional[List[int]]
