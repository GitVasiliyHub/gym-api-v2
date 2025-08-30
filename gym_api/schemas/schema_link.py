from typing import Optional

from pydantic import BaseModel, ConfigDict, Field


class CreateLink(BaseModel):
    link: str
    title: Optional[str]
    master_id: int = Field(default=1)


class Link(BaseModel):
    link_id: int
    link: str
    title: Optional[str]
    master_id: int

    model_config = ConfigDict(from_attributes=True)


class LinkExercise(BaseModel):
    link_id: int
    exercise_id: int
