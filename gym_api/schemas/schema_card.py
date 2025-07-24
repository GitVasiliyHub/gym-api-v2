from typing import Optional, List
from datetime import datetime
from enum import Enum

from pydantic import BaseModel, ConfigDict

from .schema_exercise import Exercise, ExerciseDesc
from .schema_user import Master

class CardStatus(str, Enum):
    active = 'active'
    archive = 'archive'


class Card(BaseModel):
    card_id: int
    master_id: int
    exercise_id: Optional[int]
    exercise_desc_id: Optional[int]
    create_dttm: datetime
    update_dttm: Optional[datetime]
    status: CardStatus
    title: Optional[str]

    model_config = ConfigDict(from_attributes=True)


class LinkCard(BaseModel):
    link_id: int
    card_id: int
    create_dttm: datetime
    close_dttm: Optional[datetime]


class Link(BaseModel):
    link_id: int
    title: Optional[str]
    create_dttm: datetime
    close_dttm: Optional[datetime]


class CardAggregate(Card):
    exercise: Optional[Exercise]
    exercise_des: Optional[ExerciseDesc]
    links: Optional[List[Link]]
    master: Master

    model_config = ConfigDict(from_attributes=True)
