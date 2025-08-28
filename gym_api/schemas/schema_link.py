from typing import Optional

from pydantic import BaseModel, ConfigDict


class CreateLink(BaseModel):
    link: str
    title: Optional[str]


class Link(BaseModel):
    link_id: int
    link: str
    title: Optional[str]

    model_config = ConfigDict(from_attributes=True)


class LinkExercise(BaseModel):
    link_id: int
    exercise_id: int
