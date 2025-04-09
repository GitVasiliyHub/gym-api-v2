from typing import List, Union, Optional

from pydantic import BaseModel

class InSet(BaseModel):
    numField: int
    value: Union[str, int]
    
class Exercise(BaseModel):
    week: int
    day: int
    muscles: str
    desc: str
    exercise: str
    weight: str
    rest: str
    repeats: Optional[str] = None
    exerciseIdx: Optional[int]
    sets: List[Union[str, int, InSet]]  
  
class InExerciseRow(BaseModel):
    week: int
    day: int
    muscles: str
    desc: str
    exercise: str
    weight: str
    sets: List[InSet]

class DayProgram(BaseModel):
    day: int
    muscles: str
    exercises: List[InExerciseRow]
    
class WeeProgram(BaseModel):
    week: int
    days: List[DayProgram]
    