from enum import Enum
from typing import Optional, List

from pydantic import BaseModel, ConfigDict, Field

from .schema_link import Link


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


class ExerciseAggregate(Exercise):
    links: List[Link] = Field(
        default_factory=list
    )

    model_config = ConfigDict(from_attributes=True)


class CreateExercise(BaseModel):
    master_id: int
    exercise_name: Optional[str]
    description: Optional[str]
    status: ExerciseStatus = ExerciseStatus.active
    
    link_ids: Optional[List[int]]
