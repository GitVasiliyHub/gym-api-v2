import json
from typing import Optional

from typing import List
from fastapi import APIRouter

from ..manager.dataframe import DataFrameManager
from ..schemas import exercise as model


router = APIRouter()

@router.get('/history')
def history():
    manager = DataFrameManager()
    exercises: List[model.Exercise] = manager.history()
    weeks = {}
    """
    week = {
        1: {
            1: DayProgram,
            2: DayProgram
        },
        2: {
            1: DayProgram,
            2: DayProgram
        }
    }
    """
    for ex in exercises:
        week = weeks.get(ex.week)
        new_ex = model.InExerciseRow(
            week=ex.week,
            day=ex.day,
            desc=ex.desc,
            muscles=ex.muscles,
            exercise=ex.exercise,
            weight=ex.weight,
            sets=[
                model.InSet(numField=i+1, value=ex.sets[i])
                for i in range(len(ex.sets))
            ]
        )
        if week:
            day = week.get(ex.day)
            if day: day.exercises.append(new_ex)
            else:
                week[ex.day] = model.DayProgram(
                    day=ex.day,
                    muscles=ex.muscles,
                    exercises=[new_ex]
                )
        else:
            weeks[ex.week] = {
                ex.day: model.DayProgram(
                    day=ex.day,
                    muscles=ex.muscles,
                    exercises=[new_ex]
                )}           
    result = []
    for week, days in weeks.items():           
        result.append(model.WeeProgram(
            week=week,
            days=list(days.values())
        ).dict())
    return json.dumps(result, ensure_ascii=False).encode('utf8')


@router.get('/current')
def current(week: int, day: int):
    manager = DataFrameManager()
    exercises: List[dict] = manager.current_tarin(week, day)
    return json.dumps(exercises, ensure_ascii=False).encode('utf8')


@router.get('/update')
def update_set(week: int, day: int, st: int, ex_idx: int, value: str):
    manager = DataFrameManager()
    manager.update(week=week, tr=day, st=st, ex=ex_idx, value=value)
    manager.save_dataframe()
    return 'ok', 200
    