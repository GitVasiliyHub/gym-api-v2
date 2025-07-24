from pydantic import BaseModel, ConfigDict


class Exercise(BaseModel):
    exercise_id: int
    title: str

    model_config = ConfigDict(from_attributes=True)


class ExerciseDesc(BaseModel):
    exercise_desc_id: int
    title: str

    model_config = ConfigDict(from_attributes=True)
